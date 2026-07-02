"""Organizations router — full CRUD for organization management."""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.organization import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from app.services.organization_service import OrganizationService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[OrganizationResponse], summary="List Organizations")
def list_organizations(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List organizations. System admins see all; others see their own."""
    ctx.require_role("system_admin", "org_admin", "operations_manager", "warehouse_manager", "inventory_manager")
    svc = OrganizationService(db)
    skip = (page - 1) * per_page
    items = svc.list_all(skip=skip, limit=per_page)
    from app.repositories.organization_repository import OrganizationRepository
    from app.models.organization import Organization
    total = OrganizationRepository(Organization, db).count()
    return PaginatedResponse(
        data=[OrganizationResponse.model_validate(o) for o in items],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, total_pages=max(1, -(-total // per_page))),
    )


@router.post("", response_model=SuccessResponse[OrganizationResponse], status_code=201, summary="Create Organization")
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Create a new organization. System admin only."""
    ctx.require_role("system_admin")
    svc = OrganizationService(db)
    org = svc.create(data)
    db.commit()
    db.refresh(org)
    return SuccessResponse(data=OrganizationResponse.model_validate(org), message="Organization created")


@router.get("/{org_id}", response_model=SuccessResponse[OrganizationResponse], summary="Get Organization")
def get_organization(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Get a single organization by ID."""
    ctx.require_role("system_admin", "org_admin", "operations_manager", "warehouse_manager", "inventory_manager")
    svc = OrganizationService(db)
    org = svc.get_by_id(org_id)
    return SuccessResponse(data=OrganizationResponse.model_validate(org))


@router.put("/{org_id}", response_model=SuccessResponse[OrganizationResponse], summary="Update Organization")
def update_organization(
    org_id: uuid.UUID,
    data: OrganizationUpdate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Update organization details."""
    ctx.require_role("system_admin", "org_admin")
    svc = OrganizationService(db)
    org = svc.update(org_id, data)
    db.commit()
    db.refresh(org)
    return SuccessResponse(data=OrganizationResponse.model_validate(org), message="Organization updated")
