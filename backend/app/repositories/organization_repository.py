"""Organization repository."""
from typing import List, Optional

from sqlalchemy import select

from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):

    def get_by_name(self, name: str) -> Optional[Organization]:
        stmt = select(Organization).where(Organization.name == name)
        return self.db.scalar(stmt)

    def get_active(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        stmt = (
            select(Organization)
            .where(Organization.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def name_exists(self, name: str) -> bool:
        return self.get_by_name(name) is not None
