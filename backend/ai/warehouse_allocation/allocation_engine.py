"""
Warehouse Allocation Engine (v1).
Scores warehouses using stock coverage, proximity, and capacity utilization.
Extension path: add cost matrix, time windows, priority scoring.
"""
import math
from typing import List, Tuple

from ai.interfaces.base_allocator import BaseAllocator
from ai.schemas.ai_schemas import (
    AllocationItemResult,
    AllocationOutput,
    AllocationRequest,
    WarehouseStockInput,
)

# Scoring weights — adjustable without interface changes
_WEIGHT_COVERAGE = 0.70
_WEIGHT_PROXIMITY = 0.20
_WEIGHT_CAPACITY = 0.10


class WarehouseAllocationEngine(BaseAllocator):
    """
    Multi-factor warehouse allocation engine (v1).

    Score = coverage * 0.70 + proximity * 0.20 + capacity * 0.10
    """

    def allocate(self, request: AllocationRequest) -> AllocationOutput:
        if not request.warehouses:
            raise ValueError("No warehouses provided for allocation")

        best_warehouse, best_score = self._score_warehouses(request)
        items = self._compute_allocation_items(request, best_warehouse)
        fulfilled = sum(1 for i in items if i.is_fulfilled)
        coverage_pct = (fulfilled / len(items) * 100) if items else 0.0

        explanation = (
            f"Selected '{best_warehouse.warehouse_name}' with composite score {best_score:.3f}. "
            f"Stock coverage: {coverage_pct:.1f}% of order items can be fulfilled. "
            f"Weights applied — coverage: {_WEIGHT_COVERAGE*100:.0f}%, "
            f"proximity: {_WEIGHT_PROXIMITY*100:.0f}%, "
            f"capacity utilization: {_WEIGHT_CAPACITY*100:.0f}%."
        )

        return AllocationOutput(
            order_id=request.order_id,
            warehouse_id=best_warehouse.warehouse_id,
            warehouse_name=best_warehouse.warehouse_name,
            score=round(best_score, 4),
            coverage_percentage=round(coverage_pct, 2),
            items=items,
            explanation=explanation,
        )

    def _score_warehouses(
        self, request: AllocationRequest
    ) -> Tuple[WarehouseStockInput, float]:
        best = request.warehouses[0]
        best_score = -1.0
        for warehouse in request.warehouses:
            score = self._compute_score(request, warehouse)
            if score > best_score:
                best_score = score
                best = warehouse
        return best, best_score

    def _compute_score(
        self, request: AllocationRequest, warehouse: WarehouseStockInput
    ) -> float:
        return (
            self._coverage_score(request, warehouse) * _WEIGHT_COVERAGE
            + self._proximity_score(request, warehouse) * _WEIGHT_PROXIMITY
            + self._capacity_score(warehouse) * _WEIGHT_CAPACITY
        )

    @staticmethod
    def _coverage_score(
        request: AllocationRequest, warehouse: WarehouseStockInput
    ) -> float:
        if not request.items:
            return 0.0
        fulfilled = sum(
            1 for item in request.items
            if warehouse.stock_by_product.get(item.product_id, 0.0) >= item.quantity
        )
        return fulfilled / len(request.items)

    @staticmethod
    def _proximity_score(
        request: AllocationRequest, warehouse: WarehouseStockInput
    ) -> float:
        if any(v is None for v in [
            request.delivery_latitude, request.delivery_longitude,
            warehouse.latitude, warehouse.longitude
        ]):
            return 0.5  # Neutral when coordinates unavailable
        dist = _haversine_km(
            request.delivery_latitude, request.delivery_longitude,
            warehouse.latitude, warehouse.longitude,
        )
        return max(0.0, 1.0 - dist / 1000.0)

    @staticmethod
    def _capacity_score(warehouse: WarehouseStockInput) -> float:
        if not warehouse.capacity:
            return 1.0
        utilization = sum(warehouse.stock_by_product.values()) / warehouse.capacity
        return max(0.0, 1.0 - utilization)

    @staticmethod
    def _compute_allocation_items(
        request: AllocationRequest, warehouse: WarehouseStockInput
    ) -> List[AllocationItemResult]:
        return [
            AllocationItemResult(
                product_id=item.product_id,
                requested_quantity=item.quantity,
                allocated_quantity=min(
                    warehouse.stock_by_product.get(item.product_id, 0.0), item.quantity
                ),
                is_fulfilled=(
                    warehouse.stock_by_product.get(item.product_id, 0.0) >= item.quantity
                ),
            )
            for item in request.items
        ]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
