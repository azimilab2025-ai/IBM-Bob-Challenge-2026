"""Warehouse repository."""
import uuid
from typing import List, Optional

from sqlalchemy import select

from app.models.warehouse import Warehouse
from app.repositories.base_repository import BaseRepository


class WarehouseRepository(BaseRepository[Warehouse]):

    def get_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Warehouse]:
        stmt = (
            select(Warehouse)
            .where(
                Warehouse.organization_id == organization_id,
                Warehouse.is_active == True,  # noqa: E712
            )
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def count_by_org(self, organization_id: uuid.UUID) -> int:
        from sqlalchemy import func
        stmt = (
            select(func.count())
            .select_from(Warehouse)
            .where(Warehouse.organization_id == organization_id)
        )
        return self.db.scalar(stmt) or 0

    def get_by_id_and_org(
        self, warehouse_id: uuid.UUID, organization_id: uuid.UUID
    ) -> Optional[Warehouse]:
        stmt = select(Warehouse).where(
            Warehouse.id == warehouse_id,
            Warehouse.organization_id == organization_id,
        )
        return self.db.scalar(stmt)

    def code_exists_in_org(self, code: str, organization_id: uuid.UUID) -> bool:
        stmt = select(Warehouse).where(
            Warehouse.code == code,
            Warehouse.organization_id == organization_id,
        )
        return self.db.scalar(stmt) is not None
