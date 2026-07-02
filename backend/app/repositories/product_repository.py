"""Product repository."""
import uuid
from typing import List, Optional

from sqlalchemy import select

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def get_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        stmt = (
            select(Product)
            .where(
                Product.organization_id == organization_id,
                Product.is_active == True,  # noqa: E712
            )
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def count_by_org(self, organization_id: uuid.UUID) -> int:
        from sqlalchemy import func
        stmt = (
            select(func.count())
            .select_from(Product)
            .where(Product.organization_id == organization_id)
        )
        return self.db.scalar(stmt) or 0

    def get_by_id_and_org(
        self, product_id: uuid.UUID, organization_id: uuid.UUID
    ) -> Optional[Product]:
        stmt = select(Product).where(
            Product.id == product_id,
            Product.organization_id == organization_id,
        )
        return self.db.scalar(stmt)

    def sku_exists_in_org(self, sku: str, organization_id: uuid.UUID) -> bool:
        stmt = select(Product).where(
            Product.sku == sku,
            Product.organization_id == organization_id,
        )
        return self.db.scalar(stmt) is not None
