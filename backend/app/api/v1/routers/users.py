"""Users router — user management within an organization."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserResponse], summary="List Users")
def list_users(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List users in the current user's organization."""
    ctx.require_role("system_admin", "org_admin")
    org_id = ctx.resolve_org_id()
    svc = UserService(db)
    skip = (page - 1) * per_page
    items = svc.list_by_org(org_id, skip=skip, limit=per_page)
    from app.repositories.user_repository import UserRepository
    from app.models.user import User
    total = UserRepository(User, db).count_by_org(org_id)
    return PaginatedResponse(
        data=[UserResponse.model_validate(u) for u in items],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, total_pages=max(1, -(-total // per_page))),
    )


@router.post("", response_model=SuccessResponse[UserResponse], status_code=201, summary="Create User")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Create a new user. Org admin and system admin only."""
    ctx.require_role("system_admin", "org_admin")
    # Non-system-admins can only create users in their own org
    if not ctx.is_system_admin:
        data = data.model_copy(update={"organization_id": ctx.org_uuid})
    svc = UserService(db)
    user = svc.create(data)
    db.commit()
    db.refresh(user)
    return SuccessResponse(data=UserResponse.model_validate(user), message="User created")


@router.get("/{user_id}", response_model=SuccessResponse[UserResponse], summary="Get User")
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Get user by ID."""
    ctx.require_role("system_admin", "org_admin")
    svc = UserService(db)
    user = svc.get_by_id(user_id)
    return SuccessResponse(data=UserResponse.model_validate(user))


@router.put("/{user_id}", response_model=SuccessResponse[UserResponse], summary="Update User")
def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Update user details or role."""
    ctx.require_role("system_admin", "org_admin")
    svc = UserService(db)
    user = svc.update(user_id, data)
    db.commit()
    db.refresh(user)
    return SuccessResponse(data=UserResponse.model_validate(user), message="User updated")
