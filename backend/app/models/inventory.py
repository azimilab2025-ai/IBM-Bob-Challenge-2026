"""InventoryItem model — stock level of a product in a warehouse."""
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.warehouse import Warehouse


class InventoryItem(Base, BaseModel):
    __tablename__ = "inventory_items"

    __table_args__ = (
        UniqueConstraint("product_id", "warehouse_id", name="uq_inventory_product_warehouse"),
    )

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
    quantity_on_hand: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quantity_reserved: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reorder_point: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    safety_stock: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_counted_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="inventory_items")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="inventory_items")

    @property
    def quantity_available(self) -> float:
        """Stock available for new orders (on-hand minus reserved)."""
        return max(0.0, self.quantity_on_hand - self.quantity_reserved)

    @property
    def is_low_stock(self) -> bool:
        """True if available quantity is at or below reorder point."""
        if self.reorder_point is None:
            return False
        return self.quantity_available <= self.reorder_point

    def __repr__(self) -> str:
        return (
            f"<InventoryItem product={self.product_id} "
            f"warehouse={self.warehouse_id} qty={self.quantity_on_hand}>"
        )
