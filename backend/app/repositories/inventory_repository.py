"""Inventory repository."""
import uuid
from typing import List, Optional

from sqlalchemy import select

from app.models.inventory import InventoryItem
from app.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository[InventoryItem]):

    def get_by_product_and_warehouse(
        self, product_id: uuid.UUID, warehouse_id: uuid.UUID
    ) -> Optional[InventoryItem]:
        stmt = select(InventoryItem).where(
            InventoryItem.product_id == product_id,
            InventoryItem.warehouse_id == warehouse_id,
        )
        return self.db.scalar(stmt)

    def get_by_warehouse(
        self, warehouse_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[InventoryItem]:
        stmt = (
            select(InventoryItem)
            .where(InventoryItem.warehouse_id == warehouse_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_by_product(self, product_id: uuid.UUID) -> List[InventoryItem]:
        stmt = select(InventoryItem).where(InventoryItem.product_id == product_id)
        return list(self.db.scalars(stmt).all())

    def get_low_stock_by_org(self, organization_id: uuid.UUID) -> List[InventoryItem]:
        """Return items where available qty <= reorder_point and reorder_point is set."""
        from app.models.warehouse import Warehouse
        from sqlalchemy import and_
        stmt = (
            select(InventoryItem)
            .join(Warehouse, InventoryItem.warehouse_id == Warehouse.id)
            .where(
                Warehouse.organization_id == organization_id,
                InventoryItem.reorder_point != None,  # noqa: E711
                (InventoryItem.quantity_on_hand - InventoryItem.quantity_reserved)
                <= InventoryItem.reorder_point,
            )
        )
        return list(self.db.scalars(stmt).all())

    def get_by_org_warehouses(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[InventoryItem]:
        from app.models.warehouse import Warehouse
        stmt = (
            select(InventoryItem)
            .join(Warehouse, InventoryItem.warehouse_id == Warehouse.id)
            .where(Warehouse.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())
