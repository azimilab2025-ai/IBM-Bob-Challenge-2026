"""Inventory service."""
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.models.inventory import InventoryItem
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.repositories.product_repository import ProductRepository
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.schemas.inventory import InventoryCreate, InventoryUpdate


class InventoryService:

    def __init__(self, db: Session) -> None:
        self._repo = InventoryRepository(InventoryItem, db)
        self._wh_repo = WarehouseRepository(Warehouse, db)
        self._prod_repo = ProductRepository(Product, db)
        self._db = db

    def create_or_update(self, data: InventoryCreate) -> InventoryItem:
        """Create a new inventory record or update if already exists."""
        existing = self._repo.get_by_product_and_warehouse(
            data.product_id, data.warehouse_id
        )
        if existing:
            existing.quantity_on_hand = data.quantity_on_hand
            if data.reorder_point is not None:
                existing.reorder_point = data.reorder_point
            if data.safety_stock is not None:
                existing.safety_stock = data.safety_stock
            self._db.flush()
            self._db.refresh(existing)
            return existing

        item = InventoryItem(
            product_id=data.product_id,
            warehouse_id=data.warehouse_id,
            quantity_on_hand=data.quantity_on_hand,
            reorder_point=data.reorder_point,
            safety_stock=data.safety_stock,
        )
        return self._repo.create(item)

    def adjust_quantity(self, item_id: uuid.UUID, delta: float) -> InventoryItem:
        item = self._repo.get_by_id(item_id)
        if not item:
            raise NotFoundError("InventoryItem", item_id)
        new_qty = item.quantity_on_hand + delta
        if new_qty < 0:
            raise ValidationError(
                f"Adjustment would result in negative inventory: {new_qty:.2f}"
            )
        item.quantity_on_hand = new_qty
        self._db.flush()
        self._db.refresh(item)
        return item

    def get_by_id(self, item_id: uuid.UUID) -> InventoryItem:
        item = self._repo.get_by_id(item_id)
        if not item:
            raise NotFoundError("InventoryItem", item_id)
        return item

    def list_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[InventoryItem]:
        return self._repo.get_by_org_warehouses(organization_id, skip=skip, limit=limit)

    def list_low_stock(self, organization_id: uuid.UUID) -> List[InventoryItem]:
        return self._repo.get_low_stock_by_org(organization_id)
