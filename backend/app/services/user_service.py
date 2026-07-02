"""User service — business logic for user management."""
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    def __init__(self, db: Session) -> None:
        self._repo = UserRepository(User, db)
        self._db = db

    def create(self, data: UserCreate) -> User:
        normalized_email = data.email.lower().strip()
        if self._repo.email_exists(normalized_email):
            raise ConflictError(f"User with email '{normalized_email}' already exists")

        user = User(
            email=normalized_email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            role=data.role,
            organization_id=data.organization_id,
            is_active=True,
        )
        return self._repo.create(user)

    def get_by_id(self, user_id: uuid.UUID) -> User:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    def list_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return self._repo.get_by_org(organization_id, skip=skip, limit=limit)

    def update(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(user, field, value)
        self._db.flush()
        self._db.refresh(user)
        return user
