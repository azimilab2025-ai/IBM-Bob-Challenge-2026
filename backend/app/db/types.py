"""
Cross-dialect UUID column type.

Uses the native PostgreSQL UUID type when the dialect is PostgreSQL,
and CHAR(36) with string coercion on all other dialects (e.g., SQLite
for testing).  Both representations expose python-side uuid.UUID objects
so that application code never needs to know which dialect is in use.
"""
import uuid as _uuid_module
from typing import Any, Optional

from sqlalchemy import Dialect, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator


class UUIDType(TypeDecorator):
    """
    Platform-independent UUID column.

    Storage:
        - PostgreSQL  → native UUID column (as_uuid=True)
        - Everything else (SQLite, …) → CHAR(36), stored as hyphenated string
    """

    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> Any:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(String(36))

    def process_bind_param(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[Any]:
        if value is None:
            return None
        if dialect.name == "postgresql":
            # SQLAlchemy handles native UUID objects directly
            return value if isinstance(value, _uuid_module.UUID) else _uuid_module.UUID(str(value))
        # For SQLite / others: store as lowercase hyphenated string
        if isinstance(value, _uuid_module.UUID):
            return str(value)
        return str(_uuid_module.UUID(str(value)))

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[_uuid_module.UUID]:
        if value is None:
            return None
        if isinstance(value, _uuid_module.UUID):
            return value
        return _uuid_module.UUID(str(value))
