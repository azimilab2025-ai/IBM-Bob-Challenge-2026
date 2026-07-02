"""Organization service — business logic for organization management."""
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationService:

    def __init__(self, db: Session) -> None:
        self._repo = OrganizationRepository(Organization, db)
        self._db = db

    def create(self, data: OrganizationCreate) -> Organization:
        if self._repo.name_exists(data.name):
            raise ConflictError(f"Organization with name '{data.name}' already exists")

        org = Organization(**data.model_dump())
        return self._repo.create(org)

    def get_by_id(self, org_id: uuid.UUID) -> Organization:
        org = self._repo.get_by_id(org_id)
        if not org:
            raise NotFoundError("Organization", org_id)
        return org

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        return self._repo.get_active(skip=skip, limit=limit)

    def update(self, org_id: uuid.UUID, data: OrganizationUpdate) -> Organization:
        org = self.get_by_id(org_id)
        updates = data.model_dump(exclude_unset=True)

        if "name" in updates and updates["name"] != org.name:
            if self._repo.name_exists(updates["name"]):
                raise ConflictError(f"Organization name '{updates['name']}' is already taken")

        for field, value in updates.items():
            setattr(org, field, value)

        self._db.flush()
        self._db.refresh(org)
        return org
