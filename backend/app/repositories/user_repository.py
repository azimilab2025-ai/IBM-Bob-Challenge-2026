"""User repository — all database access for User model."""
import uuid
from typing import List, Optional

from sqlalchemy import select

from app.models.user import User, UserRole
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def get_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[User]:
        stmt = (
            select(User)
            .where(User.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def count_by_org(self, organization_id: uuid.UUID) -> int:
        from sqlalchemy import func
        from sqlalchemy import select as sa_select
        stmt = (
            sa_select(func.count())
            .select_from(User)
            .where(User.organization_id == organization_id)
        )
        return self.db.scalar(stmt) or 0

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None
