"""AI result models — persisted outputs from AI modules."""
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.warehouse import Warehouse
    from app.models.product import Product


class WarehouseAllocationResult(Base, BaseModel):
    """Stores the AI-generated warehouse allocation decision for an order."""
    __tablename__ = "warehouse_allocation_results"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    coverage_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    allocation_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="allocation_results")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="allocation_results")


class DemandForecast(Base, BaseModel):
    """Stores demand forecast output for a product."""
    __tablename__ = "demand_forecasts"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    forecast_method: Mapped[str] = mapped_column(String(100), nullable=False)
    forecast_horizon_days: Mapped[int] = mapped_column(Integer, nullable=False)
    forecast_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product")


class InventoryRecommendation(Base, BaseModel):
    """Stores inventory optimization recommendations."""
    __tablename__ = "inventory_recommendations"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    safety_stock: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reorder_point: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    recommended_order_quantity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expected_holding_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expected_shortage_risk: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product")


class RouteOptimizationResult(Base, BaseModel):
    """Stores route optimization results for a set of orders."""
    __tablename__ = "route_optimization_results"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    route_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    total_distance_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
