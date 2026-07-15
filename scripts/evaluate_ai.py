#!/usr/bin/env python3
"""
Deterministic evaluation runner for the project's existing AI modules.

Purpose:
- Execute the current forecasting, inventory optimization, warehouse allocation,
  and route optimization implementations without changing their logic.
- Produce a reproducible, evidence-based snapshot for README documentation.
- Use only deterministic synthetic demo data and the project's existing code.

This script:
- does not connect to the database;
- does not call the live API;
- does not modify project files;
- does not require new third-party dependencies.

Run from the repository root:

    python3 scripts/evaluate_ai.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

# Make backend/ importable when this script is executed from the repository root
# or directly from another working directory.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = REPOSITORY_ROOT / "backend"

if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from ai.demand_forecasting.moving_average import MovingAverageForecaster
from ai.inventory_optimization.eoq_optimizer import EOQOptimizer
from ai.route_optimization.basic_router import NearestNeighborRouter
from ai.schemas.ai_schemas import (
    AllocationRequest,
    DeliveryStop,
    ForecastInput,
    HistoricalDataPoint,
    InventoryOptimizationInput,
    OrderItemInput,
    RouteInput,
    WarehouseStockInput,
)
from ai.warehouse_allocation.allocation_engine import WarehouseAllocationEngine


SCENARIO_NAME = "Deterministic Synthetic Supply-Chain Evaluation Scenario"
SEPARATOR = "=" * 78
SUBSEPARATOR = "-" * 78


def evaluate_forecasting() -> Dict[str, Any]:
    """
    Evaluate the current moving-average implementation.

    The complete seven-point history is used for the documented seven-day
    forecast. A one-step holdout evaluation is also performed: the final actual
    value is withheld, predicted from the preceding values, and compared using
    absolute error (equivalent to MAE for one observation).
    """
    quantities = [16.0, 18.0, 20.0, 21.0, 19.0, 23.0, 25.0]
    historical_data = [
        HistoricalDataPoint(date=f"2026-01-{day:02d}", quantity=quantity)
        for day, quantity in enumerate(quantities, start=1)
    ]

    forecaster = MovingAverageForecaster()

    forecast_input = ForecastInput(
        product_id="SKU-DEMO-001",
        historical_data=historical_data,
        horizon_days=7,
        window_size=7,
    )
    forecast_output = forecaster.predict(forecast_input)

    holdout_input = ForecastInput(
        product_id="SKU-DEMO-001",
        historical_data=historical_data[:-1],
        horizon_days=1,
        window_size=3,
    )
    holdout_output = forecaster.predict(holdout_input)

    predicted_holdout = holdout_output.daily_forecasts[0].predicted_quantity
    actual_holdout = historical_data[-1].quantity
    sample_mae = abs(actual_holdout - predicted_holdout)

    return {
        "module": "Demand Forecasting",
        "method": forecast_output.method,
        "historical_values": quantities,
        "window_size": forecast_input.window_size,
        "forecast_horizon_days": forecast_output.horizon_days,
        "predicted_daily_demand": forecast_output.daily_forecasts[
            0
        ].predicted_quantity,
        "total_predicted_demand": forecast_output.total_predicted_demand,
        "holdout_actual": actual_holdout,
        "holdout_prediction": predicted_holdout,
        "sample_mae": round(sample_mae, 2),
        "confidence": forecast_output.daily_forecasts[0].confidence,
        "explanation": forecast_output.explanation,
    }


def evaluate_inventory_optimization() -> Dict[str, Any]:
    """Evaluate the current EOQ-based inventory optimizer."""
    optimizer = EOQOptimizer()

    optimization_input = InventoryOptimizationInput(
        product_id="SKU-DEMO-001",
        warehouse_id="WH-BERLIN-01",
        average_daily_demand=12.0,
        demand_std_dev=6.5,
        lead_time_days=5.0,
        service_level=0.95,
        holding_cost_per_unit=15.0,
        shortage_cost_per_unit=10.0,
        annual_order_cost=16.0,
    )
    output = optimizer.optimize(optimization_input)

    return {
        "module": "Inventory Optimization",
        "average_daily_demand": optimization_input.average_daily_demand,
        "demand_std_dev": optimization_input.demand_std_dev,
        "lead_time_days": optimization_input.lead_time_days,
        "service_level": optimization_input.service_level,
        "safety_stock": output.safety_stock,
        "reorder_point": output.reorder_point,
        "recommended_order_quantity": output.recommended_order_quantity,
        "expected_holding_cost": output.expected_holding_cost,
        "expected_shortage_risk": output.expected_shortage_risk,
        "explanation": output.explanation,
    }


def _allocation_request(
    warehouses: List[WarehouseStockInput],
) -> AllocationRequest:
    return AllocationRequest(
        order_id="ORDER-DEMO-001",
        delivery_latitude=52.5200,
        delivery_longitude=13.4050,
        items=[
            OrderItemInput(product_id="SKU-DEMO-001", quantity=50.0),
            OrderItemInput(product_id="SKU-DEMO-002", quantity=20.0),
        ],
        warehouses=warehouses,
    )


def evaluate_warehouse_allocation() -> Dict[str, Any]:
    """
    Evaluate the current warehouse allocation engine.

    Candidate scores are obtained through the engine's public allocate method,
    one warehouse at a time. The complete request is then evaluated to verify
    the selected warehouse.
    """
    warehouses = [
        WarehouseStockInput(
            warehouse_id="WH-BERLIN-WEST",
            warehouse_name="Berlin West Fulfillment Center",
            latitude=52.5601,
            longitude=13.0897,
            capacity=1000,
            stock_by_product={
                "SKU-DEMO-001": 120.0,
                "SKU-DEMO-002": 80.0,
            },
        ),
        WarehouseStockInput(
            warehouse_id="WH-LEIPZIG",
            warehouse_name="Leipzig Regional Hub",
            latitude=51.3397,
            longitude=12.3731,
            capacity=500,
            stock_by_product={
                "SKU-DEMO-001": 200.0,
                "SKU-DEMO-002": 100.0,
            },
        ),
        WarehouseStockInput(
            warehouse_id="WH-POTSDAM",
            warehouse_name="Potsdam Distribution Depot",
            latitude=52.3906,
            longitude=13.0645,
            capacity=1000,
            stock_by_product={
                "SKU-DEMO-001": 30.0,
                "SKU-DEMO-002": 100.0,
            },
        ),
    ]

    engine = WarehouseAllocationEngine()

    candidate_results = []
    for warehouse in warehouses:
        result = engine.allocate(_allocation_request([warehouse]))
        candidate_results.append(
            {
                "warehouse_id": result.warehouse_id,
                "warehouse_name": result.warehouse_name,
                "score": result.score,
                "coverage_percentage": result.coverage_percentage,
            }
        )

    ranked_candidates = sorted(
        candidate_results,
        key=lambda item: item["score"],
        reverse=True,
    )
    selected = engine.allocate(_allocation_request(warehouses))

    return {
        "module": "Warehouse Allocation",
        "selected_warehouse_id": selected.warehouse_id,
        "selected_warehouse_name": selected.warehouse_name,
        "selected_score": selected.score,
        "selected_coverage_percentage": selected.coverage_percentage,
        "second_best_warehouse_id": ranked_candidates[1]["warehouse_id"],
        "second_best_warehouse_name": ranked_candidates[1]["warehouse_name"],
        "second_best_score": ranked_candidates[1]["score"],
        "score_gap": round(
            ranked_candidates[0]["score"] - ranked_candidates[1]["score"],
            4,
        ),
        "ranked_candidates": ranked_candidates,
        "explanation": selected.explanation,
    }


def _haversine_km(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    """Calculate great-circle distance using the same formula as the router."""
    earth_radius_km = 6371.0
    phi_1 = math.radians(latitude_1)
    phi_2 = math.radians(latitude_2)
    delta_phi = math.radians(latitude_2 - latitude_1)
    delta_lambda = math.radians(longitude_2 - longitude_1)

    haversine_value = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi_1)
        * math.cos(phi_2)
        * math.sin(delta_lambda / 2) ** 2
    )
    return earth_radius_km * 2 * math.atan2(
        math.sqrt(haversine_value),
        math.sqrt(1 - haversine_value),
    )


def _open_route_distance_km(
    warehouse_latitude: float,
    warehouse_longitude: float,
    stops: Sequence[DeliveryStop],
) -> float:
    """
    Calculate warehouse-to-stops distance without a return leg.

    This matches the current NearestNeighborRouter behavior.
    """
    current_latitude = warehouse_latitude
    current_longitude = warehouse_longitude
    total_distance = 0.0

    for stop in stops:
        if stop.latitude is None or stop.longitude is None:
            raise ValueError(
                f"Stop {stop.order_id} has no coordinates; distance cannot be measured."
            )

        total_distance += _haversine_km(
            current_latitude,
            current_longitude,
            stop.latitude,
            stop.longitude,
        )
        current_latitude = stop.latitude
        current_longitude = stop.longitude

    return total_distance


def evaluate_route_optimization() -> Dict[str, Any]:
    """Compare the current input order with the current nearest-neighbor output."""
    warehouse_latitude = 52.5200
    warehouse_longitude = 13.4050

    initial_stops = [
        DeliveryStop(
            order_id="ORDER-POTSDAM",
            delivery_address="Potsdam",
            latitude=52.3906,
            longitude=13.0645,
        ),
        DeliveryStop(
            order_id="ORDER-ORANIENBURG",
            delivery_address="Oranienburg",
            latitude=52.7558,
            longitude=13.2419,
        ),
        DeliveryStop(
            order_id="ORDER-ERKNER",
            delivery_address="Erkner",
            latitude=52.4200,
            longitude=13.7500,
        ),
        DeliveryStop(
            order_id="ORDER-FALKENSEE",
            delivery_address="Falkensee",
            latitude=52.5601,
            longitude=13.0897,
        ),
    ]

    initial_distance = _open_route_distance_km(
        warehouse_latitude,
        warehouse_longitude,
        initial_stops,
    )

    router = NearestNeighborRouter()
    route_output = router.optimize(
        RouteInput(
            warehouse_id="WH-BERLIN-01",
            warehouse_latitude=warehouse_latitude,
            warehouse_longitude=warehouse_longitude,
            stops=initial_stops,
        )
    )

    if route_output.total_distance_km is None:
        raise RuntimeError(
            "The route optimizer did not return a measurable route distance."
        )

    optimized_distance = route_output.total_distance_km
    improvement_km = initial_distance - optimized_distance
    improvement_percentage = (
        improvement_km / initial_distance * 100 if initial_distance > 0 else 0.0
    )

    return {
        "module": "Route Optimization",
        "algorithm": "nearest_neighbor",
        "distance_scope": "Open route: warehouse to all stops; no return leg",
        "initial_sequence": [stop.order_id for stop in initial_stops],
        "optimized_sequence": [stop.order_id for stop in route_output.stops],
        "initial_distance_km": round(initial_distance, 2),
        "optimized_distance_km": round(optimized_distance, 2),
        "distance_saved_km": round(improvement_km, 2),
        "improvement_percentage": round(improvement_percentage, 2),
        "estimated_duration_minutes": route_output.estimated_duration_minutes,
        "explanation": route_output.explanation,
    }


def _print_heading(title: str) -> None:
    print()
    print(SUBSEPARATOR)
    print(title)
    print(SUBSEPARATOR)


def _format_sequence(values: Sequence[str]) -> str:
    return " -> ".join(values)


def print_detailed_report(results: Dict[str, Dict[str, Any]]) -> None:
    """Print a human-readable evaluation report."""
    forecasting = results["forecasting"]
    inventory = results["inventory"]
    allocation = results["allocation"]
    routing = results["routing"]

    print(SEPARATOR)
    print("AI-POWERED SUPPLY CHAIN OPTIMIZATION PLATFORM")
    print("MEASURED AI RESULTS")
    print(SEPARATOR)
    print(f"Scenario: {SCENARIO_NAME}")
    print("Data classification: deterministic synthetic demo data")
    print("Execution mode: local, database-free, network-free, read-only")
    print("Algorithms: current project implementations; no logic modified")

    _print_heading("1. DEMAND FORECASTING")
    print(f"Method: {forecasting['method']}")
    print(f"Historical values: {forecasting['historical_values']}")
    print(f"Window size: {forecasting['window_size']} days")
    print(
        "Predicted daily demand: "
        f"{forecasting['predicted_daily_demand']:.4f} units"
    )
    print(
        f"{forecasting['forecast_horizon_days']}-day predicted demand: "
        f"{forecasting['total_predicted_demand']:.2f} units"
    )
    print(
        "One-step holdout: "
        f"predicted {forecasting['holdout_prediction']:.2f}, "
        f"actual {forecasting['holdout_actual']:.2f}"
    )
    print(f"Sample one-step MAE: {forecasting['sample_mae']:.2f} units")
    print(f"Per-point confidence: {forecasting['confidence']}")
    print(f"Explanation: {forecasting['explanation']}")

    _print_heading("2. INVENTORY OPTIMIZATION")
    print(
        f"Average daily demand: {inventory['average_daily_demand']:.2f} units"
    )
    print(f"Demand standard deviation: {inventory['demand_std_dev']:.2f}")
    print(f"Lead time: {inventory['lead_time_days']:.2f} days")
    print(f"Service level: {inventory['service_level'] * 100:.1f}%")
    print(f"Safety stock: {inventory['safety_stock']:.2f} units")
    print(f"Reorder point: {inventory['reorder_point']:.2f} units")
    print(
        "Recommended order quantity: "
        f"{inventory['recommended_order_quantity']:.2f} units"
    )
    print(
        f"Expected holding cost: ${inventory['expected_holding_cost']:.2f}"
    )
    print(
        "Expected shortage risk: "
        f"{inventory['expected_shortage_risk'] * 100:.1f}%"
    )
    print(f"Explanation: {inventory['explanation']}")

    _print_heading("3. WAREHOUSE ALLOCATION")
    print(
        "Selected warehouse: "
        f"{allocation['selected_warehouse_name']} "
        f"({allocation['selected_warehouse_id']})"
    )
    print(f"Selected score: {allocation['selected_score']:.4f}")
    print(
        "Selected coverage: "
        f"{allocation['selected_coverage_percentage']:.2f}%"
    )
    print(
        "Second-best warehouse: "
        f"{allocation['second_best_warehouse_name']} "
        f"({allocation['second_best_warehouse_id']})"
    )
    print(f"Second-best score: {allocation['second_best_score']:.4f}")
    print(f"Score gap: {allocation['score_gap']:.4f}")
    print("Candidate ranking:")
    for position, candidate in enumerate(
        allocation["ranked_candidates"],
        start=1,
    ):
        print(
            f"  {position}. {candidate['warehouse_name']} — "
            f"score {candidate['score']:.4f}, "
            f"coverage {candidate['coverage_percentage']:.2f}%"
        )
    print(f"Explanation: {allocation['explanation']}")

    _print_heading("4. ROUTE OPTIMIZATION")
    print(f"Algorithm: {routing['algorithm']}")
    print(f"Distance scope: {routing['distance_scope']}")
    print(
        "Initial sequence: "
        f"{_format_sequence(routing['initial_sequence'])}"
    )
    print(
        "Optimized sequence: "
        f"{_format_sequence(routing['optimized_sequence'])}"
    )
    print(f"Initial distance: {routing['initial_distance_km']:.2f} km")
    print(
        f"Optimized distance: {routing['optimized_distance_km']:.2f} km"
    )
    print(f"Distance saved: {routing['distance_saved_km']:.2f} km")
    print(
        f"Measured improvement: {routing['improvement_percentage']:.2f}%"
    )
    print(
        "Estimated duration: "
        f"{routing['estimated_duration_minutes']} minutes"
    )
    print(f"Explanation: {routing['explanation']}")


def print_markdown_snapshot(results: Dict[str, Dict[str, Any]]) -> None:
    """Print a README-ready Markdown table using the measured results."""
    forecasting = results["forecasting"]
    inventory = results["inventory"]
    allocation = results["allocation"]
    routing = results["routing"]

    _print_heading("README-READY MEASURED RESULTS SNAPSHOT")
    print(
        "> Measured using the current deterministic synthetic demo scenario. "
        "No KPI below is a production claim."
    )
    print()
    print("| Decision Area | Measured Input | Current System Result | Evidence |")
    print("|---|---|---|---|")
    print(
        "| Demand Forecasting | "
        f"7 historical values; {forecasting['window_size']}-day window; "
        f"{forecasting['forecast_horizon_days']}-day horizon | "
        f"{forecasting['total_predicted_demand']:.2f} units predicted; "
        f"{forecasting['predicted_daily_demand']:.4f} units/day; "
        f"one-step sample MAE {forecasting['sample_mae']:.2f} units | "
        "`MovingAverageForecaster` |"
    )
    print(
        "| Inventory Optimization | "
        f"{inventory['average_daily_demand']:.0f} units/day; "
        f"{inventory['lead_time_days']:.0f}-day lead time; "
        f"{inventory['service_level'] * 100:.0f}% service level | "
        f"Safety stock {inventory['safety_stock']:.2f}; "
        f"reorder point {inventory['reorder_point']:.2f}; "
        f"recommended order {inventory['recommended_order_quantity']:.2f} units | "
        "`EOQOptimizer` |"
    )
    print(
        "| Warehouse Allocation | "
        "2 order items; 3 candidate warehouses | "
        f"Selected score {allocation['selected_score']:.4f}; "
        f"second-best {allocation['second_best_score']:.4f}; "
        f"score gap {allocation['score_gap']:.4f}; "
        f"coverage {allocation['selected_coverage_percentage']:.0f}% | "
        "`WarehouseAllocationEngine` |"
    )
    print(
        "| Route Optimization | "
        "1 warehouse; 4 delivery stops; open-route distance | "
        f"{routing['initial_distance_km']:.2f} km initial; "
        f"{routing['optimized_distance_km']:.2f} km optimized; "
        f"{routing['distance_saved_km']:.2f} km saved; "
        f"{routing['improvement_percentage']:.2f}% improvement | "
        "`NearestNeighborRouter` |"
    )

    print()
    print("Limitations:")
    print(
        "- The dataset is deterministic and synthetic; results demonstrate "
        "current system behavior rather than production performance."
    )
    print(
        "- The forecasting MAE is a transparent one-step sample holdout, "
        "not a multi-period production benchmark."
    )
    print(
        "- Route distance follows the current implementation and excludes "
        "a return leg to the warehouse."
    )
    print(
        "- Warehouse scores reflect the current configured coverage, "
        "proximity, and capacity weights."
    )


def main() -> int:
    try:
        results = {
            "forecasting": evaluate_forecasting(),
            "inventory": evaluate_inventory_optimization(),
            "allocation": evaluate_warehouse_allocation(),
            "routing": evaluate_route_optimization(),
        }
        print_detailed_report(results)
        print_markdown_snapshot(results)
        print()
        print(SEPARATOR)
        print("Evaluation completed successfully.")
        print(SEPARATOR)
        return 0
    except Exception as error:
        print(
            f"Evaluation failed: {error.__class__.__name__}: {error}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
