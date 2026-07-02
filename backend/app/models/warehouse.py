"""Warehouse model — physical or virtual storage location."""
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel
from app.db.types import UUIDType

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.inventory import InventoryItem
    from app.models.ai_results import WarehouseAllocationResult


class Warehouse(Base, BaseModel):
    __tablename__ = "warehouses"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="warehouses")
    inventory_items: Mapped[List["InventoryItem"]] = relationship(
        "InventoryItem", back_populates="warehouse"
    )
    allocation_results: Mapped[List["WarehouseAllocationResult"]] = relationship(
        "WarehouseAllocationResult", back_populates="warehouse"
    )

    def __repr__(self) -> str:
        return f"<Warehouse id={self.id} name='{self.name}' org={self.organization_id}>"
