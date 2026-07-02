"""Unit tests for AI modules — no DB dependency."""
import pytest

from ai.demand_forecasting.moving_average import MovingAverageForecaster
from ai.inventory_optimization.eoq_optimizer import EOQOptimizer
from ai.warehouse_allocation.allocation_engine import WarehouseAllocationEngine
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


# ---------------------------------------------------------------------------
# Moving Average Forecaster
# ---------------------------------------------------------------------------

class TestMovingAverageForecaster:

    def test_predict_with_data(self):
        forecaster = MovingAverageForecaster()
        result = forecaster.predict(ForecastInput(
            product_id="p1",
            historical_data=[
                HistoricalDataPoint(date="2025-01-01", quantity=100.0),
                HistoricalDataPoint(date="2025-01-02", quantity=80.0),
            ],
            horizon_days=7,
            window_size=2,
        ))
        assert result.horizon_days == 7
        assert len(result.daily_forecasts) == 7
        assert result.total_predicted_demand == pytest.approx(7 * 90.0, rel=0.01)
        assert result.method == "moving_average"
        assert result.explanation != ""

    def test_predict_no_data(self):
        forecaster = MovingAverageForecaster()
        result = forecaster.predict(ForecastInput(
            product_id="p1", historical_data=[], horizon_days=5, window_size=7
        ))
        assert result.total_predicted_demand == 0.0
        assert all(p.predicted_quantity == 0.0 for p in result.daily_forecasts)

    def test_window_clipped_to_available_data(self):
        forecaster = MovingAverageForecaster()
        result = forecaster.predict(ForecastInput(
            product_id="p1",
            historical_data=[HistoricalDataPoint(date="2025-01-01", quantity=50.0)],
            horizon_days=3,
            window_size=10,  # larger than available data
        ))
        assert result.total_predicted_demand == pytest.approx(3 * 50.0, rel=0.01)


# ---------------------------------------------------------------------------
# EOQ Optimizer
# ---------------------------------------------------------------------------

class TestEOQOptimizer:

    def test_basic_optimization(self):
        opt = EOQOptimizer()
        result = opt.optimize(InventoryOptimizationInput(
            product_id="p1",
            warehouse_id="w1",
            average_daily_demand=50.0,
            demand_std_dev=10.0,
            lead_time_days=7.0,
            service_level=0.95,
        ))
        assert result.safety_stock > 0
        assert result.reorder_point > result.safety_stock
        assert result.recommended_order_quantity > 0
        assert result.expected_holding_cost > 0
        assert 0 <= result.expected_shortage_risk <= 1.0
        assert result.explanation != ""

    def test_zero_demand(self):
        opt = EOQOptimizer()
        result = opt.optimize(InventoryOptimizationInput(
            product_id="p1", warehouse_id="w1",
            average_daily_demand=0.0, demand_std_dev=0.0, lead_time_days=5.0,
        ))
        assert result.safety_stock == 0.0
        assert result.recommended_order_quantity >= 1.0  # minimum floor

    def test_reorder_point_formula(self):
        """ROP = avg_daily * lead_time + safety_stock."""
        opt = EOQOptimizer()
        result = opt.optimize(InventoryOptimizationInput(
            product_id="p1", warehouse_id="w1",
            average_daily_demand=20.0, demand_std_dev=2.0, lead_time_days=10.0,
            service_level=0.95,
        ))
        expected_rop = 20.0 * 10.0 + result.safety_stock
        assert result.reorder_point == pytest.approx(expected_rop, rel=0.01)


# ---------------------------------------------------------------------------
# Warehouse Allocation Engine
# ---------------------------------------------------------------------------

class TestWarehouseAllocationEngine:

    def test_full_coverage_warehouse_selected(self):
        engine = WarehouseAllocationEngine()
        result = engine.allocate(AllocationRequest(
            order_id="o1",
            delivery_latitude=None,
            delivery_longitude=None,
            items=[OrderItemInput(product_id="p1", quantity=10.0)],
            warehouses=[
                WarehouseStockInput(
                    warehouse_id="w1", warehouse_name="Full WH",
                    latitude=None, longitude=None, capacity=1000,
                    stock_by_product={"p1": 50.0},
                ),
                WarehouseStockInput(
                    warehouse_id="w2", warehouse_name="Empty WH",
                    latitude=None, longitude=None, capacity=1000,
                    stock_by_product={"p1": 0.0},
                ),
            ],
        ))
        assert result.warehouse_id == "w1"
        assert result.coverage_percentage == 100.0

    def test_no_warehouses_raises(self):
        engine = WarehouseAllocationEngine()
        with pytest.raises(ValueError):
            engine.allocate(AllocationRequest(
                order_id="o1", delivery_latitude=None, delivery_longitude=None,
                items=[OrderItemInput(product_id="p1", quantity=1.0)],
                warehouses=[],
            ))

    def test_proximity_scoring_prefers_closest(self):
        engine = WarehouseAllocationEngine()
        result = engine.allocate(AllocationRequest(
            order_id="o1",
            delivery_latitude=40.0,
            delivery_longitude=30.0,
            items=[OrderItemInput(product_id="p1", quantity=5.0)],
            warehouses=[
                WarehouseStockInput(
                    warehouse_id="w_near", warehouse_name="Near WH",
                    latitude=40.1, longitude=30.1, capacity=None,
                    stock_by_product={"p1": 100.0},
                ),
                WarehouseStockInput(
                    warehouse_id="w_far", warehouse_name="Far WH",
                    latitude=50.0, longitude=50.0, capacity=None,
                    stock_by_product={"p1": 100.0},
                ),
            ],
        ))
        assert result.warehouse_id == "w_near"

    def test_explanation_provided(self):
        engine = WarehouseAllocationEngine()
        result = engine.allocate(AllocationRequest(
            order_id="o1", delivery_latitude=None, delivery_longitude=None,
            items=[OrderItemInput(product_id="p1", quantity=1.0)],
            warehouses=[WarehouseStockInput(
                warehouse_id="w1", warehouse_name="WH1",
                latitude=None, longitude=None, capacity=None,
                stock_by_product={"p1": 10.0},
            )],
        ))
        assert len(result.explanation) > 0


# ---------------------------------------------------------------------------
# Route Optimizer
# ---------------------------------------------------------------------------

class TestNearestNeighborRouter:

    def test_empty_stops(self):
        router = NearestNeighborRouter()
        result = router.optimize(RouteInput(
            warehouse_id="w1", warehouse_latitude=None, warehouse_longitude=None, stops=[]
        ))
        assert result.stops == []
        assert result.total_distance_km == 0.0

    def test_single_stop(self):
        router = NearestNeighborRouter()
        result = router.optimize(RouteInput(
            warehouse_id="w1",
            warehouse_latitude=40.0, warehouse_longitude=30.0,
            stops=[DeliveryStop(order_id="o1", delivery_address="Main St", latitude=40.1, longitude=30.1)],
        ))
        assert len(result.stops) == 1
        assert result.stops[0].sequence == 1

    def test_route_order_nearest_first(self):
        router = NearestNeighborRouter()
        result = router.optimize(RouteInput(
            warehouse_id="w1",
            warehouse_latitude=0.0, warehouse_longitude=0.0,
            stops=[
                DeliveryStop(order_id="far", delivery_address=None, latitude=10.0, longitude=10.0),
                DeliveryStop(order_id="near", delivery_address=None, latitude=1.0, longitude=1.0),
            ],
        ))
        # Nearest stop should come first
        assert result.stops[0].order_id == "near"
        assert result.total_distance_km is not None
        assert result.total_distance_km > 0
