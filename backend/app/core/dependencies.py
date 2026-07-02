"""
FastAPI dependency providers.
All shared dependencies (DB session, current user context) are defined here.
Routers import only from here — no auth logic lives in routers.
"""
import uuid
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.db.session import get_db

_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> str:
    """Extract validated user_id string from JWT. Used by auth router."""
    if credentials is None:
        raise AuthenticationError("Authorization header is required")
    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise AuthenticationError("Refresh token cannot be used for API access")
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Token missing subject claim")
    return user_id


async def get_current_user_context(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> "CurrentUserContext":
    """
    Resolve full user context (user_id, role, org_id) from JWT.
    Use in all routers that need authorization checks.
    """
    if credentials is None:
        raise AuthenticationError("Authorization header is required")
    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise AuthenticationError("Refresh token cannot be used for API access")
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Token missing subject claim")
    role = payload.get("role", "")
    org_id = payload.get("org_id")
    return CurrentUserContext(
        user_id=user_id,
        role=role,
        organization_id=org_id,
        is_system_admin=(role == "system_admin"),
    )


class CurrentUserContext:
    """Resolved user context — injected by get_current_user_context dependency."""

    def __init__(
        self,
        user_id: str,
        role: str,
        organization_id: Optional[str],
        is_system_admin: bool,
    ) -> None:
        self.user_id = user_id
        self.role = role
        self.organization_id = organization_id
        self.is_system_admin = is_system_admin

    @property
    def user_uuid(self) -> uuid.UUID:
        return uuid.UUID(self.user_id)

    @property
    def org_uuid(self) -> Optional[uuid.UUID]:
        return uuid.UUID(self.organization_id) if self.organization_id else None

    def require_role(self, *roles: str) -> None:
        if self.is_system_admin:
            return
        if self.role not in roles:
            raise AuthorizationError(
                f"This action requires one of the following roles: {', '.join(roles)}"
            )

    def require_organization_access(self, org_id: str) -> None:
        if self.is_system_admin:
            return
        if self.organization_id != org_id:
            raise AuthorizationError("Access denied to this organization's resources")

    def resolve_org_id(self, requested_org_id: Optional[uuid.UUID] = None) -> uuid.UUID:
        """Return effective org_id: system_admin may supply any, others use their own."""
        if self.is_system_admin and requested_org_id is not None:
            return requested_org_id
        if not self.org_uuid:
            raise AuthorizationError("User is not associated with any organization")
        return self.org_uuid
