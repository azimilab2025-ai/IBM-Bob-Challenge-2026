"""Dashboard router — management KPI summary."""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import SuccessResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/summary", response_model=SuccessResponse[dict], summary="Dashboard Summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """
    Return KPIs and operational overview for the management dashboard.
    Includes: total warehouses, products, orders, low-stock items,
    inventory value, recent orders, and operational alerts.
    """
    org_id = ctx.resolve_org_id()
    svc = DashboardService(db)
    summary = svc.get_summary(org_id)
    return SuccessResponse(
        data={
            "total_warehouses": summary.total_warehouses,
            "total_products": summary.total_products,
            "total_orders": summary.total_orders,
            "pending_orders": summary.pending_orders,
            "low_stock_items": summary.low_stock_items,
            "total_inventory_value": summary.total_inventory_value,
            "recent_orders": summary.recent_orders,
            "operational_alerts": summary.operational_alerts,
        },
        message="Dashboard summary retrieved",
    )


@router.get("/alerts", response_model=SuccessResponse[list], summary="Operational Alerts")
def operational_alerts(
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Return active operational alerts for the organization."""
    org_id = ctx.resolve_org_id()
    svc = DashboardService(db)
    summary = svc.get_summary(org_id)
    return SuccessResponse(
        data=summary.operational_alerts,
        message=f"{len(summary.operational_alerts)} active alert(s)",
    )
