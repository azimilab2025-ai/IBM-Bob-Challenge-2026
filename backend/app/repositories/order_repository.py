"""Order repository."""
import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):

    def get_by_id_with_items(self, order_id: uuid.UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return self.db.scalar(stmt)

    def get_by_org(
        self,
        organization_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[OrderStatus] = None,
    ) -> List[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.organization_id == organization_id)
        )
        if status:
            stmt = stmt.where(Order.status == status)
        stmt = stmt.order_by(Order.created_at.desc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count_by_org(self, organization_id: uuid.UUID) -> int:
        from sqlalchemy import func
        stmt = (
            select(func.count())
            .select_from(Order)
            .where(Order.organization_id == organization_id)
        )
        return self.db.scalar(stmt) or 0

    def count_pending_by_org(self, organization_id: uuid.UUID) -> int:
        from sqlalchemy import func
        stmt = (
            select(func.count())
            .select_from(Order)
            .where(
                Order.organization_id == organization_id,
                Order.status == OrderStatus.PENDING,
            )
        )
        return self.db.scalar(stmt) or 0

    def reference_exists(self, reference_number: str) -> bool:
        stmt = select(Order).where(Order.reference_number == reference_number)
        return self.db.scalar(stmt) is not None
