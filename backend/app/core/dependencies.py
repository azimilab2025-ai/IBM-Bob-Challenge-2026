"""
FastAPI dependency providers.
All shared dependencies (DB session, current user, role checks) are defined here.
"""
import uuid
from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.db.session import get_db

_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> str:
    """
    Extract and validate the current user ID from the Authorization header.
    Raises AuthenticationError if no valid token is provided.
    """
    if credentials is None:
        raise AuthenticationError("Authorization header is required")

    payload = decode_token(credentials.credentials)

    if payload.get("type") != "access":
        raise AuthenticationError("Refresh token cannot be used for API access")

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Token missing subject claim")

    return user_id


class CurrentUserContext:
    """
    Resolved user context injected into service layer.
    Carries user_id, role, and organization_id for authorization checks.
    """

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

    def require_role(self, *roles: str) -> None:
        """Raise AuthorizationError if user does not have one of the required roles."""
        if self.is_system_admin:
            return
        if self.role not in roles:
            raise AuthorizationError(
                f"This action requires one of the following roles: {', '.join(roles)}"
            )

    def require_organization_access(self, org_id: str) -> None:
        """Raise AuthorizationError if user does not belong to the organization."""
        if self.is_system_admin:
            return
        if self.organization_id != org_id:
            raise AuthorizationError("Access denied to this organization's resources")
