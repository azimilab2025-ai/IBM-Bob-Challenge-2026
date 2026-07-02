"""
EOQ-based Inventory Optimizer.
Calculates safety stock, reorder point, and economic order quantity.
Extension path: stochastic demand models, multi-echelon optimization.

Uses statistics only from the standard library to avoid heavy dependencies
at the AI module level. scipy is NOT imported here to keep AI modules lightweight.
"""
import math
from typing import Optional

from ai.interfaces.base_optimizer import BaseInventoryOptimizer
from ai.schemas.ai_schemas import InventoryOptimizationInput, InventoryOptimizationOutput

# z-score table for common service levels (avoids scipy dependency in AI layer)
_SERVICE_LEVEL_Z = {
    0.80: 0.842,
    0.85: 1.036,
    0.90: 1.282,
    0.95: 1.645,
    0.97: 1.881,
    0.98: 2.054,
    0.99: 2.326,
    0.999: 3.090,
}


def _z_score(service_level: float) -> float:
    """Return the z-score for a given service level using a lookup table."""
    # Find nearest key
    nearest = min(_SERVICE_LEVEL_Z.keys(), key=lambda k: abs(k - service_level))
    return _SERVICE_LEVEL_Z[nearest]


class EOQOptimizer(BaseInventoryOptimizer):
    """
    Economic Order Quantity inventory optimizer (v1).

    Formulas:
      Safety Stock  = Z * σ * √L
      Reorder Point = (avg_daily * L) + safety_stock
      EOQ           = √(2 * D_annual * S / H)
    """

    def optimize(self, input_data: InventoryOptimizationInput) -> InventoryOptimizationOutput:
        z = _z_score(input_data.service_level)
        safety_stock = self._safety_stock(z, input_data.demand_std_dev, input_data.lead_time_days)
        reorder_point = self._reorder_point(
            input_data.average_daily_demand, input_data.lead_time_days, safety_stock
        )
        eoq = self._eoq(
            input_data.average_daily_demand,
            input_data.annual_order_cost,
            input_data.holding_cost_per_unit,
        )
        holding_cost = (eoq / 2) * input_data.holding_cost_per_unit
        shortage_risk = round(1.0 - input_data.service_level, 4)

        explanation = (
            f"Service level {input_data.service_level*100:.0f}% → Z-score {z:.3f}. "
            f"Safety stock: {safety_stock:.1f} units (covers demand variability over {input_data.lead_time_days}-day lead time). "
            f"Reorder point: {reorder_point:.1f} units (trigger new order when stock reaches this level). "
            f"EOQ: {eoq:.1f} units per order (minimizes total holding + ordering cost). "
            f"Estimated annual holding cost: ${holding_cost:.2f}. "
            f"Expected shortage risk: {shortage_risk*100:.1f}%."
        )

        return InventoryOptimizationOutput(
            product_id=input_data.product_id,
            warehouse_id=input_data.warehouse_id,
            safety_stock=round(safety_stock, 2),
            reorder_point=round(reorder_point, 2),
            recommended_order_quantity=round(eoq, 2),
            expected_holding_cost=round(holding_cost, 2),
            expected_shortage_risk=shortage_risk,
            explanation=explanation,
        )

    @staticmethod
    def _safety_stock(z: float, std_dev: float, lead_time: float) -> float:
        return max(0.0, z * std_dev * math.sqrt(max(0.0, lead_time)))

    @staticmethod
    def _reorder_point(avg_daily: float, lead_time: float, safety_stock: float) -> float:
        return avg_daily * lead_time + safety_stock

    @staticmethod
    def _eoq(avg_daily: float, order_cost: float, holding_cost: float) -> float:
        annual_demand = avg_daily * 365
        if holding_cost <= 0 or annual_demand <= 0:
            return max(1.0, annual_demand)
        return max(1.0, math.sqrt(2 * annual_demand * order_cost / holding_cost))
