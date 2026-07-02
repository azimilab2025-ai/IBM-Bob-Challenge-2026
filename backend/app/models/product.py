"""Product model — catalog item within an organization."""
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.inventory import InventoryItem
    from app.models.order import OrderItem


class Product(Base, BaseModel):
    __tablename__ = "products"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    unit: Mapped[str] = mapped_column(String(50), default="unit", nullable=False)
    unit_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reorder_point: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lead_time_days: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="products")
    inventory_items: Mapped[List["InventoryItem"]] = relationship(
        "InventoryItem", back_populates="product"
    )
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product")

    def __repr__(self) -> str:
        return f"<Product id={self.id} sku='{self.sku}' name='{self.name}'>"
