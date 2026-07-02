"""Organization model — top-level multi-tenant entity."""
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.warehouse import Warehouse
    from app.models.product import Product
    from app.models.order import Order


class Organization(Base, BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="organization")
    warehouses: Mapped[List["Warehouse"]] = relationship("Warehouse", back_populates="organization")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="organization")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="organization")

    def __repr__(self) -> str:
        return f"<Organization id={self.id} name='{self.name}'>"
