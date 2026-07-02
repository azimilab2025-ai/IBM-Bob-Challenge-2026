"""Order and OrderItem models — demand entry point for the supply chain."""
import uuid
from typing import TYPE_CHECKING, List, Optional
import enum

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.product import Product
    from app.models.user import User
    from app.models.ai_results import WarehouseAllocationResult


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ALLOCATED = "allocated"
    IN_PROGRESS = "in_progress"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderPriority(str, enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Order(Base, BaseModel):
    __tablename__ = "orders"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    reference_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True,
    )
    priority: Mapped[OrderPriority] = mapped_column(
        Enum(OrderPriority, name="order_priority"),
        default=OrderPriority.NORMAL,
        nullable=False,
    )
    delivery_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    delivery_latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="orders")
    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    allocation_results: Mapped[List["WarehouseAllocationResult"]] = relationship(
        "WarehouseAllocationResult", back_populates="order"
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} ref='{self.reference_number}' status='{self.status}'>"


class OrderItem(Base, BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem order={self.order_id} product={self.product_id} qty={self.quantity}>"
