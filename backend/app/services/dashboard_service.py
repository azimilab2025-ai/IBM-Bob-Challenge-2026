"""Dashboard service — aggregates KPIs for the management dashboard."""
import uuid
from dataclasses import dataclass
from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.inventory import InventoryItem
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.ai_results import WarehouseAllocationResult, InventoryRecommendation


@dataclass
class DashboardSummary:
    total_warehouses: int
    total_products: int
    total_orders: int
    pending_orders: int
    low_stock_items: int
    total_inventory_value: float
    recent_orders: List[dict]
    operational_alerts: List[str]


class DashboardService:

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_summary(self, organization_id: uuid.UUID) -> DashboardSummary:
        total_warehouses = self._count(Warehouse, Warehouse.organization_id == organization_id)
        total_products = self._count(Product, Product.organization_id == organization_id)
        total_orders = self._count(Order, Order.organization_id == organization_id)
        pending_orders = self._count(
            Order,
            Order.organization_id == organization_id,
            Order.status == OrderStatus.PENDING,
        )

        # Low stock items (items where available qty <= reorder_point)
        from app.repositories.inventory_repository import InventoryRepository
        inv_repo = InventoryRepository(InventoryItem, self._db)
        low_stock_items = len(inv_repo.get_low_stock_by_org(organization_id))

        # Inventory value estimate
        total_inventory_value = self._calculate_inventory_value(organization_id)

        # Recent orders (last 5)
        recent_orders = self._get_recent_orders(organization_id)

        # Operational alerts
        alerts = []
        if low_stock_items > 0:
            alerts.append(f"{low_stock_items} product(s) are at or below reorder point")
        if pending_orders > 0:
            alerts.append(f"{pending_orders} order(s) pending processing")

        return DashboardSummary(
            total_warehouses=total_warehouses,
            total_products=total_products,
            total_orders=total_orders,
            pending_orders=pending_orders,
            low_stock_items=low_stock_items,
            total_inventory_value=total_inventory_value,
            recent_orders=recent_orders,
            operational_alerts=alerts,
        )

    def _count(self, model, *conditions) -> int:
        stmt = select(func.count()).select_from(model)
        for condition in conditions:
            stmt = stmt.where(condition)
        return self._db.scalar(stmt) or 0

    def _calculate_inventory_value(self, organization_id: uuid.UUID) -> float:
        stmt = (
            select(
                func.sum(InventoryItem.quantity_on_hand * Product.unit_cost)
            )
            .join(Product, InventoryItem.product_id == Product.id)
            .join(Warehouse, InventoryItem.warehouse_id == Warehouse.id)
            .where(
                Warehouse.organization_id == organization_id,
                Product.unit_cost != None,  # noqa: E711
            )
        )
        result = self._db.scalar(stmt)
        return round(result or 0.0, 2)

    def _get_recent_orders(self, organization_id: uuid.UUID) -> List[dict]:
        stmt = (
            select(Order)
            .where(Order.organization_id == organization_id)
            .order_by(Order.created_at.desc())
            .limit(5)
        )
        orders = list(self._db.scalars(stmt).all())
        return [
            {
                "id": str(o.id),
                "reference_number": o.reference_number,
                "status": o.status.value,
                "priority": o.priority.value,
                "total_amount": o.total_amount,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in orders
        ]
