"""Orders router — order creation and lifecycle management."""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.models.order import OrderStatus
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[OrderResponse], summary="List Orders")
def list_orders(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    status: Optional[OrderStatus] = Query(default=None),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List orders for the current organization with optional status filter."""
    org_id = ctx.resolve_org_id()
    svc = OrderService(db)
    skip = (page - 1) * per_page
    items = svc.list_by_org(org_id, skip=skip, limit=per_page, status=status)
    from app.repositories.order_repository import OrderRepository
    from app.models.order import Order
    total = OrderRepository(Order, db).count_by_org(org_id)
    return PaginatedResponse(
        data=[OrderResponse.model_validate(o) for o in items],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, total_pages=max(1, -(-total // per_page))),
    )


@router.post("", response_model=SuccessResponse[OrderResponse], status_code=201, summary="Create Order")
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Create a new order with one or more items."""
    org_id = ctx.resolve_org_id()
    svc = OrderService(db)
    order = svc.create(org_id, ctx.user_uuid, data)
    db.commit()
    db.refresh(order)
    return SuccessResponse(data=OrderResponse.model_validate(order), message="Order created")


@router.get("/{order_id}", response_model=SuccessResponse[OrderResponse], summary="Get Order")
def get_order(
    order_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Get a single order with its items."""
    org_id = ctx.resolve_org_id()
    svc = OrderService(db)
    order = svc.get_by_id(order_id, org_id)
    return SuccessResponse(data=OrderResponse.model_validate(order))


@router.patch("/{order_id}", response_model=SuccessResponse[OrderResponse], summary="Update Order")
def update_order(
    order_id: uuid.UUID,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Update order status, priority, or delivery info."""
    ctx.require_role("system_admin", "org_admin", "operations_manager")
    org_id = ctx.resolve_org_id()
    svc = OrderService(db)
    order = svc.update_status(order_id, org_id, data)
    db.commit()
    db.refresh(order)
    return SuccessResponse(data=OrderResponse.model_validate(order), message="Order updated")


@router.post("/{order_id}/allocate", response_model=SuccessResponse[dict], summary="Allocate Warehouse")
def allocate_order(
    order_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Trigger AI warehouse allocation for this order."""
    ctx.require_role("system_admin", "org_admin", "operations_manager")
    org_id = ctx.resolve_org_id()
    from app.services.ai_service import AIService
    svc = AIService(db)
    result = svc.allocate_order(order_id, org_id)
    db.commit()
    return SuccessResponse(
        data={
            "result_id": str(result.id),
            "order_id": str(result.order_id),
            "warehouse_id": str(result.warehouse_id),
            "score": result.score,
            "coverage_percentage": result.coverage_percentage,
            "explanation": result.explanation,
        },
        message="Warehouse allocation completed",
    )
