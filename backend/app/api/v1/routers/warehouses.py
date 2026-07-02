"""Warehouses router — warehouse management within an organization."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse, WarehouseUpdate
from app.services.warehouse_service import WarehouseService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[WarehouseResponse], summary="List Warehouses")
def list_warehouses(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List active warehouses for the current organization."""
    org_id = ctx.resolve_org_id()
    svc = WarehouseService(db)
    skip = (page - 1) * per_page
    items = svc.list_by_org(org_id, skip=skip, limit=per_page)
    from app.repositories.warehouse_repository import WarehouseRepository
    from app.models.warehouse import Warehouse
    total = WarehouseRepository(Warehouse, db).count_by_org(org_id)
    return PaginatedResponse(
        data=[WarehouseResponse.model_validate(w) for w in items],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, total_pages=max(1, -(-total // per_page))),
    )


@router.post("", response_model=SuccessResponse[WarehouseResponse], status_code=201, summary="Create Warehouse")
def create_warehouse(
    data: WarehouseCreate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Create a new warehouse in the current organization."""
    ctx.require_role("system_admin", "org_admin", "warehouse_manager")
    org_id = ctx.resolve_org_id()
    svc = WarehouseService(db)
    wh = svc.create(org_id, data)
    db.commit()
    db.refresh(wh)
    return SuccessResponse(data=WarehouseResponse.model_validate(wh), message="Warehouse created")


@router.get("/{warehouse_id}", response_model=SuccessResponse[WarehouseResponse], summary="Get Warehouse")
def get_warehouse(
    warehouse_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Get a single warehouse by ID."""
    org_id = ctx.resolve_org_id()
    svc = WarehouseService(db)
    wh = svc.get_by_id(warehouse_id, org_id)
    return SuccessResponse(data=WarehouseResponse.model_validate(wh))


@router.put("/{warehouse_id}", response_model=SuccessResponse[WarehouseResponse], summary="Update Warehouse")
def update_warehouse(
    warehouse_id: uuid.UUID,
    data: WarehouseUpdate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Update warehouse details."""
    ctx.require_role("system_admin", "org_admin", "warehouse_manager")
    org_id = ctx.resolve_org_id()
    svc = WarehouseService(db)
    wh = svc.update(warehouse_id, org_id, data)
    db.commit()
    db.refresh(wh)
    return SuccessResponse(data=WarehouseResponse.model_validate(wh), message="Warehouse updated")


@router.delete("/{warehouse_id}", response_model=SuccessResponse[WarehouseResponse], summary="Deactivate Warehouse")
def deactivate_warehouse(
    warehouse_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Soft-delete (deactivate) a warehouse."""
    ctx.require_role("system_admin", "org_admin")
    org_id = ctx.resolve_org_id()
    svc = WarehouseService(db)
    wh = svc.deactivate(warehouse_id, org_id)
    db.commit()
    return SuccessResponse(data=WarehouseResponse.model_validate(wh), message="Warehouse deactivated")
