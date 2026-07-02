"""
AI orchestration service.
Bridges business layer with AI modules. Translates domain objects to AI input schemas,
calls AI modules through their interfaces, and persists results.
"""
import uuid
from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from ai.demand_forecasting.moving_average import MovingAverageForecaster
from ai.warehouse_allocation.allocation_engine import WarehouseAllocationEngine
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

from app.core.exceptions import NotFoundError, ValidationError
from app.models.inventory import InventoryItem
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.ai_results import (
    DemandForecast,
    InventoryRecommendation,
    RouteOptimizationResult,
    WarehouseAllocationResult,
)
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.warehouse_repository import WarehouseRepository


class AIService:

    def __init__(self, db: Session) -> None:
        self._db = db
        self._inv_repo = InventoryRepository(InventoryItem, db)
        self._order_repo = OrderRepository(Order, db)
        self._prod_repo = ProductRepository(Product, db)
        self._wh_repo = WarehouseRepository(Warehouse, db)

    # ------------------------------------------------------------------
    # Warehouse Allocation
    # ------------------------------------------------------------------

    def allocate_order(
        self, order_id: uuid.UUID, organization_id: uuid.UUID
    ) -> WarehouseAllocationResult:
        order = self._order_repo.get_by_id_with_items(order_id)
        if not order or order.organization_id != organization_id:
            raise NotFoundError("Order", order_id)

        warehouses = self._wh_repo.get_by_org(organization_id)
        if not warehouses:
            raise ValidationError("No active warehouses found in this organization")

        wh_inputs = []
        for wh in warehouses:
            stock = {}
            for inv_item in self._inv_repo.get_by_warehouse(wh.id):
                stock[str(inv_item.product_id)] = inv_item.quantity_available
            wh_inputs.append(WarehouseStockInput(
                warehouse_id=str(wh.id),
                warehouse_name=wh.name,
                latitude=wh.latitude,
                longitude=wh.longitude,
                capacity=wh.capacity,
                stock_by_product=stock,
            ))

        request = AllocationRequest(
            order_id=str(order.id),
            delivery_latitude=order.delivery_latitude,
            delivery_longitude=order.delivery_longitude,
            items=[
                OrderItemInput(product_id=str(i.product_id), quantity=i.quantity)
                for i in order.items
            ],
            warehouses=wh_inputs,
        )

        result = WarehouseAllocationEngine().allocate(request)

        db_result = WarehouseAllocationResult(
            order_id=order.id,
            warehouse_id=uuid.UUID(result.warehouse_id),
            score=result.score,
            coverage_percentage=result.coverage_percentage,
            explanation=result.explanation,
            allocation_details={
                "items": [
                    {
                        "product_id": i.product_id,
                        "requested": i.requested_quantity,
                        "allocated": i.allocated_quantity,
                        "fulfilled": i.is_fulfilled,
                    }
                    for i in result.items
                ]
            },
        )
        self._db.add(db_result)
        order.status = OrderStatus.ALLOCATED
        self._db.flush()
        self._db.refresh(db_result)
        return db_result

    # ------------------------------------------------------------------
    # Demand Forecasting
    # ------------------------------------------------------------------

    def forecast_demand(
        self,
        product_id: uuid.UUID,
        organization_id: uuid.UUID,
        horizon_days: int = 30,
        window_size: int = 7,
    ) -> DemandForecast:
        product = self._prod_repo.get_by_id_and_org(product_id, organization_id)
        if not product:
            raise NotFoundError("Product", product_id)

        # Build historical data from past orders
        historical = self._build_historical_data(product_id, organization_id, days=90)

        forecast_input = ForecastInput(
            product_id=str(product_id),
            historical_data=historical,
            horizon_days=horizon_days,
            window_size=window_size,
        )

        result = MovingAverageForecaster().predict(forecast_input)

        db_result = DemandForecast(
            product_id=product_id,
            forecast_method=result.method,
            forecast_horizon_days=result.horizon_days,
            forecast_data={
                "daily_forecasts": [
                    {"date": p.date, "quantity": p.predicted_quantity, "confidence": p.confidence}
                    for p in result.daily_forecasts
                ],
                "total_predicted_demand": result.total_predicted_demand,
            },
            confidence=0.70 if historical else None,
            explanation=result.explanation,
        )
        self._db.add(db_result)
        self._db.flush()
        self._db.refresh(db_result)
        return db_result

    # ------------------------------------------------------------------
    # Inventory Optimization
    # ------------------------------------------------------------------

    def optimize_inventory(
        self,
        product_id: uuid.UUID,
        warehouse_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> InventoryRecommendation:
        product = self._prod_repo.get_by_id_and_org(product_id, organization_id)
        if not product:
            raise NotFoundError("Product", product_id)

        warehouse = self._wh_repo.get_by_id_and_org(warehouse_id, organization_id)
        if not warehouse:
            raise NotFoundError("Warehouse", warehouse_id)

        # Derive demand stats from order history
        historical = self._build_historical_data(product_id, organization_id, days=90)
        demands = [p.quantity for p in historical]
        avg_demand = (sum(demands) / len(demands)) if demands else 0.0
        std_dev = (
            (sum((d - avg_demand) ** 2 for d in demands) / len(demands)) ** 0.5
            if len(demands) > 1 else 0.0
        )

        opt_input = InventoryOptimizationInput(
            product_id=str(product_id),
            warehouse_id=str(warehouse_id),
            average_daily_demand=avg_demand,
            demand_std_dev=std_dev,
            lead_time_days=float(product.lead_time_days or 7),
            holding_cost_per_unit=float(product.unit_cost or 1.0) * 0.25,
            annual_order_cost=50.0,
        )

        result = EOQOptimizer().optimize(opt_input)

        db_result = InventoryRecommendation(
            product_id=product_id,
            warehouse_id=warehouse_id,
            safety_stock=result.safety_stock,
            reorder_point=result.reorder_point,
            recommended_order_quantity=result.recommended_order_quantity,
            expected_holding_cost=result.expected_holding_cost,
            expected_shortage_risk=result.expected_shortage_risk,
            explanation=result.explanation,
        )
        self._db.add(db_result)
        self._db.flush()
        self._db.refresh(db_result)
        return db_result

    # ------------------------------------------------------------------
    # Route Optimization
    # ------------------------------------------------------------------

    def optimize_routes(
        self,
        warehouse_id: uuid.UUID,
        order_ids: List[uuid.UUID],
        organization_id: uuid.UUID,
    ) -> RouteOptimizationResult:
        warehouse = self._wh_repo.get_by_id_and_org(warehouse_id, organization_id)
        if not warehouse:
            raise NotFoundError("Warehouse", warehouse_id)

        stops = []
        for oid in order_ids:
            order = self._order_repo.get_by_id_with_items(oid)
            if order and order.organization_id == organization_id:
                stops.append(DeliveryStop(
                    order_id=str(oid),
                    delivery_address=order.delivery_address,
                    latitude=order.delivery_latitude,
                    longitude=order.delivery_longitude,
                ))

        route_input = RouteInput(
            warehouse_id=str(warehouse_id),
            warehouse_latitude=warehouse.latitude,
            warehouse_longitude=warehouse.longitude,
            stops=stops,
        )

        result = NearestNeighborRouter().optimize(route_input)

        db_result = RouteOptimizationResult(
            organization_id=organization_id,
            route_data={
                "stops": [
                    {
                        "sequence": s.sequence,
                        "order_id": s.order_id,
                        "address": s.delivery_address,
                        "lat": s.latitude,
                        "lon": s.longitude,
                    }
                    for s in result.stops
                ]
            },
            total_distance_km=result.total_distance_km,
            estimated_duration_minutes=result.estimated_duration_minutes,
            explanation=result.explanation,
        )
        self._db.add(db_result)
        self._db.flush()
        self._db.refresh(db_result)
        return db_result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_historical_data(
        self, product_id: uuid.UUID, organization_id: uuid.UUID, days: int
    ) -> List[HistoricalDataPoint]:
        """Aggregate daily demand from order history."""
        from sqlalchemy import select, func as sa_func
        from app.models.order import OrderItem

        cutoff = date.today() - timedelta(days=days)

        stmt = (
            select(
                sa_func.date(Order.created_at).label("order_date"),
                sa_func.sum(OrderItem.quantity).label("total_qty"),
            )
            .join(OrderItem, OrderItem.order_id == Order.id)
            .where(
                Order.organization_id == organization_id,
                OrderItem.product_id == product_id,
                Order.created_at >= cutoff,
            )
            .group_by(sa_func.date(Order.created_at))
            .order_by(sa_func.date(Order.created_at))
        )

        rows = self._db.execute(stmt).fetchall()
        return [
            HistoricalDataPoint(date=str(row.order_date), quantity=float(row.total_qty))
            for row in rows
        ]
