"""
Authentication service.
All login, token refresh, and user context resolution logic lives here.
"""
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.core.config import get_settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, UserProfile


class AuthService:

    def __init__(self, db: Session) -> None:
        self._user_repo = UserRepository(User, db)

    def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate user credentials and return access + refresh tokens."""
        user = self._user_repo.get_by_email(email.lower().strip())

        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("Account is disabled. Contact your administrator.")

        additional_claims = {
            "role": user.role.value,
            "org_id": str(user.organization_id) if user.organization_id else None,
        }

        access_token = create_access_token(str(user.id), additional_claims)
        refresh_token = create_refresh_token(str(user.id))
        settings = get_settings()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def refresh(self, refresh_token: str) -> TokenResponse:
        """Issue a new access token from a valid refresh token."""
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token type. Provide a refresh token.")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Malformed token")

        user = self._user_repo.get_by_id(uuid.UUID(user_id))
        if not user or not user.is_active:
            raise AuthenticationError("User not found or account disabled")

        additional_claims = {
            "role": user.role.value,
            "org_id": str(user.organization_id) if user.organization_id else None,
        }

        settings = get_settings()
        new_access = create_access_token(str(user.id), additional_claims)
        new_refresh = create_refresh_token(str(user.id))

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def get_current_user(self, user_id: str) -> User:
        """Resolve user from token subject claim."""
        user = self._user_repo.get_by_id(uuid.UUID(user_id))
        if not user or not user.is_active:
            raise AuthenticationError("User not found or account disabled")
        return user

    def build_user_profile(self, user: User) -> UserProfile:
        return UserProfile(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            organization_id=str(user.organization_id) if user.organization_id else None,
        )
