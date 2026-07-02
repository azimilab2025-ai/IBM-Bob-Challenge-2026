"""Inventory router — inventory management and low-stock alerts."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.inventory import InventoryAdjust, InventoryCreate, InventoryResponse
from app.services.inventory_service import InventoryService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[InventoryResponse], summary="List Inventory")
def list_inventory(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List inventory items across all warehouses in the organization."""
    org_id = ctx.resolve_org_id()
    svc = InventoryService(db)
    skip = (page - 1) * per_page
    items = svc.list_by_org(org_id, skip=skip, limit=per_page)
    return PaginatedResponse(
        data=[_to_response(i) for i in items],
        meta=PaginationMeta(page=page, per_page=per_page, total=len(items), total_pages=1),
    )


@router.post("", response_model=SuccessResponse[InventoryResponse], status_code=201, summary="Set Inventory")
def set_inventory(
    data: InventoryCreate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Create or update inventory record for a product/warehouse pair."""
    ctx.require_role("system_admin", "org_admin", "warehouse_manager", "inventory_manager")
    svc = InventoryService(db)
    item = svc.create_or_update(data)
    db.commit()
    db.refresh(item)
    return SuccessResponse(data=_to_response(item), message="Inventory record saved")


@router.get("/alerts/low-stock", response_model=SuccessResponse[list], summary="Low Stock Alerts")
def low_stock_alerts(
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Return inventory items at or below their reorder point."""
    org_id = ctx.resolve_org_id()
    svc = InventoryService(db)
    items = svc.list_low_stock(org_id)
    return SuccessResponse(
        data=[_to_response(i) for i in items],
        message=f"{len(items)} item(s) require attention",
    )


@router.get("/{item_id}", response_model=SuccessResponse[InventoryResponse], summary="Get Inventory Item")
def get_inventory_item(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Get a single inventory record by ID."""
    svc = InventoryService(db)
    item = svc.get_by_id(item_id)
    return SuccessResponse(data=_to_response(item))


@router.post("/{item_id}/adjust", response_model=SuccessResponse[InventoryResponse], summary="Adjust Quantity")
def adjust_inventory(
    item_id: uuid.UUID,
    data: InventoryAdjust,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Adjust inventory quantity by a positive or negative delta."""
    ctx.require_role("system_admin", "org_admin", "warehouse_manager", "inventory_manager")
    svc = InventoryService(db)
    item = svc.adjust_quantity(item_id, data.delta)
    db.commit()
    db.refresh(item)
    return SuccessResponse(data=_to_response(item), message=f"Quantity adjusted by {data.delta:+.2f}")


def _to_response(item) -> InventoryResponse:
    """Map InventoryItem ORM object to InventoryResponse schema."""
    return InventoryResponse(
        id=item.id,
        product_id=item.product_id,
        warehouse_id=item.warehouse_id,
        quantity_on_hand=item.quantity_on_hand,
        quantity_reserved=item.quantity_reserved,
        quantity_available=item.quantity_available,
        reorder_point=item.reorder_point,
        safety_stock=item.safety_stock,
        is_low_stock=item.is_low_stock,
    )
