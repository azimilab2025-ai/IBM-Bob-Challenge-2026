"""Warehouse service — business logic for warehouse management."""
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.warehouse import Warehouse
from app.repositories.warehouse_repository import WarehouseRepository
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


class WarehouseService:

    def __init__(self, db: Session) -> None:
        self._repo = WarehouseRepository(Warehouse, db)
        self._db = db

    def create(self, organization_id: uuid.UUID, data: WarehouseCreate) -> Warehouse:
        if self._repo.code_exists_in_org(data.code, organization_id):
            raise ConflictError(
                f"Warehouse code '{data.code}' already exists in this organization"
            )

        warehouse = Warehouse(organization_id=organization_id, **data.model_dump())
        return self._repo.create(warehouse)

    def get_by_id(self, warehouse_id: uuid.UUID, organization_id: uuid.UUID) -> Warehouse:
        wh = self._repo.get_by_id_and_org(warehouse_id, organization_id)
        if not wh:
            raise NotFoundError("Warehouse", warehouse_id)
        return wh

    def list_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Warehouse]:
        return self._repo.get_by_org(organization_id, skip=skip, limit=limit)

    def update(
        self, warehouse_id: uuid.UUID, organization_id: uuid.UUID, data: WarehouseUpdate
    ) -> Warehouse:
        wh = self.get_by_id(warehouse_id, organization_id)
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(wh, field, value)
        self._db.flush()
        self._db.refresh(wh)
        return wh

    def deactivate(self, warehouse_id: uuid.UUID, organization_id: uuid.UUID) -> Warehouse:
        wh = self.get_by_id(warehouse_id, organization_id)
        wh.is_active = False
        self._db.flush()
        return wh
