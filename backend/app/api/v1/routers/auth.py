"""Authentication router — login, refresh, logout, current user profile."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse, UserProfile
from app.schemas.common import SuccessResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=SuccessResponse[TokenResponse], summary="Login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate with email and password. Returns access and refresh tokens."""
    svc = AuthService(db)
    tokens = svc.login(request.email, request.password)
    return SuccessResponse(data=tokens, message="Login successful")


@router.post("/refresh", response_model=SuccessResponse[TokenResponse], summary="Refresh Token")
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access + refresh token pair."""
    svc = AuthService(db)
    tokens = svc.refresh(request.refresh_token)
    return SuccessResponse(data=tokens, message="Token refreshed")


@router.get("/me", response_model=SuccessResponse[UserProfile], summary="Current User")
def get_me(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return the profile of the authenticated user."""
    svc = AuthService(db)
    user = svc.get_current_user(current_user_id)
    profile = svc.build_user_profile(user)
    return SuccessResponse(data=profile, message="Profile retrieved")
