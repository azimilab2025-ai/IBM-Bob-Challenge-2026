"""Reports router — basic operational and management reports."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.models.inventory import InventoryItem
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.schemas.common import SuccessResponse

router = APIRouter()


@router.get("/inventory", response_model=SuccessResponse[dict], summary="Inventory Report")
def inventory_report(
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """
    Inventory status report: total items, total value, low-stock count,
    and per-warehouse breakdown.
    """
    org_id = ctx.resolve_org_id()

    # Per-warehouse summary
    stmt = (
        select(
            Warehouse.id,
            Warehouse.name,
            Warehouse.code,
            func.count(InventoryItem.id).label("product_count"),
            func.sum(InventoryItem.quantity_on_hand).label("total_qty"),
            func.sum(InventoryItem.quantity_on_hand * Product.unit_cost).label("total_value"),
        )
        .join(InventoryItem, InventoryItem.warehouse_id == Warehouse.id, isouter=True)
        .join(Product, InventoryItem.product_id == Product.id, isouter=True)
        .where(Warehouse.organization_id == org_id, Warehouse.is_active == True)  # noqa: E712
        .group_by(Warehouse.id, Warehouse.name, Warehouse.code)
    )
    rows = db.execute(stmt).fetchall()

    warehouses = [
        {
            "warehouse_id": str(r.id),
            "warehouse_name": r.name,
            "warehouse_code": r.code,
            "product_count": r.product_count or 0,
            "total_quantity": float(r.total_qty or 0),
            "total_value": round(float(r.total_value or 0), 2),
        }
        for r in rows
    ]

    total_value = sum(w["total_value"] for w in warehouses)
    total_qty = sum(w["total_quantity"] for w in warehouses)

    from app.repositories.inventory_repository import InventoryRepository
    low_stock_count = len(InventoryRepository(InventoryItem, db).get_low_stock_by_org(org_id))

    return SuccessResponse(
        data={
            "summary": {
                "total_inventory_value": round(total_value, 2),
                "total_quantity": round(total_qty, 2),
                "low_stock_items": low_stock_count,
                "warehouses_count": len(warehouses),
            },
            "by_warehouse": warehouses,
        },
        message="Inventory report generated",
    )


@router.get("/orders", response_model=SuccessResponse[dict], summary="Orders Report")
def orders_report(
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Orders activity report: counts by status and recent trends."""
    org_id = ctx.resolve_org_id()

    stmt = (
        select(Order.status, func.count(Order.id).label("count"))
        .where(Order.organization_id == org_id)
        .group_by(Order.status)
    )
    rows = db.execute(stmt).fetchall()

    by_status = {r.status.value: r.count for r in rows}
    total = sum(by_status.values())

    return SuccessResponse(
        data={
            "total_orders": total,
            "by_status": by_status,
            "completion_rate": round(
                (by_status.get("delivered", 0) / total * 100) if total > 0 else 0, 1
            ),
        },
        message="Orders report generated",
    )


@router.get("/forecasts", response_model=SuccessResponse[dict], summary="Forecasts Report")
def forecasts_report(
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List recent demand forecasts for the organization's products."""
    org_id = ctx.resolve_org_id()

    from app.models.ai_results import DemandForecast
    from app.models.product import Product
    stmt = (
        select(
            DemandForecast.id,
            DemandForecast.product_id,
            Product.name.label("product_name"),
            DemandForecast.forecast_method,
            DemandForecast.forecast_horizon_days,
            DemandForecast.created_at,
        )
        .join(Product, DemandForecast.product_id == Product.id)
        .where(Product.organization_id == org_id)
        .order_by(DemandForecast.created_at.desc())
        .limit(20)
    )
    rows = db.execute(stmt).fetchall()

    return SuccessResponse(
        data={
            "forecasts": [
                {
                    "forecast_id": str(r.id),
                    "product_id": str(r.product_id),
                    "product_name": r.product_name,
                    "method": r.forecast_method,
                    "horizon_days": r.forecast_horizon_days,
                    "generated_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ]
        },
        message="Forecasts report generated",
    )
