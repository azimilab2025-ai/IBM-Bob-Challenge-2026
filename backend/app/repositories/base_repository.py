"""
Generic base repository providing common CRUD operations.
All domain repositories inherit from this class.
No business logic belongs here — only database access.
"""
import uuid
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Base CRUD repository. All repos extend this."""

    def __init__(self, model: Type[ModelT], db: Session) -> None:
        self.model = model
        self.db = db

    def get_by_id(self, record_id: uuid.UUID) -> Optional[ModelT]:
        return self.db.get(self.model, record_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelT]:
        stmt = select(self.model).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        return self.db.scalar(stmt) or 0

    def create(self, instance: ModelT) -> ModelT:
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: ModelT) -> None:
        self.db.delete(instance)
        self.db.flush()
