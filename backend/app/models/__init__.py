"""
ORM Models package.
Import all models here so Alembic autogenerate can discover them.
"""
from app.models.organization import Organization
from app.models.user import User, UserRole
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.inventory import InventoryItem
from app.models.order import Order, OrderItem, OrderStatus, OrderPriority
from app.models.ai_results import (
    WarehouseAllocationResult,
    DemandForecast,
    InventoryRecommendation,
    RouteOptimizationResult,
)
from app.models.activity_log import ActivityLog

__all__ = [
    "Organization",
    "User",
    "UserRole",
    "Warehouse",
    "Product",
    "InventoryItem",
    "Order",
    "OrderItem",
    "OrderStatus",
    "OrderPriority",
    "WarehouseAllocationResult",
    "DemandForecast",
    "InventoryRecommendation",
    "RouteOptimizationResult",
    "ActivityLog",
]
