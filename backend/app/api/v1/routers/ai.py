"""AI Insights router — demand forecasting, inventory optimization, route optimization."""
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import SuccessResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/forecast/{product_id}", response_model=SuccessResponse[dict], summary="Demand Forecast")
def demand_forecast(
    product_id: uuid.UUID,
    horizon_days: int = Query(default=30, ge=1, le=365),
    window_size: int = Query(default=7, ge=1, le=90),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """
    Generate a demand forecast for a product using historical order data.
    Returns daily predictions and total predicted demand.
    """
    org_id = ctx.resolve_org_id()
    svc = AIService(db)
    result = svc.forecast_demand(product_id, org_id, horizon_days=horizon_days, window_size=window_size)
    db.commit()
    return SuccessResponse(
        data={
            "result_id": str(result.id),
            "product_id": str(result.product_id),
            "method": result.forecast_method,
            "horizon_days": result.forecast_horizon_days,
            "forecast": result.forecast_data,
            "explanation": result.explanation,
        },
        message="Demand forecast generated",
    )


@router.post("/optimize-inventory", response_model=SuccessResponse[dict], summary="Inventory Optimization")
def optimize_inventory(
    product_id: uuid.UUID = Query(...),
    warehouse_id: uuid.UUID = Query(...),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """
    Calculate optimal safety stock, reorder point, and EOQ for a product/warehouse pair.
    Returns actionable recommendations with explanations.
    """
    org_id = ctx.resolve_org_id()
    svc = AIService(db)
    result = svc.optimize_inventory(product_id, warehouse_id, org_id)
    db.commit()
    return SuccessResponse(
        data={
            "result_id": str(result.id),
            "product_id": str(result.product_id),
            "warehouse_id": str(result.warehouse_id),
            "safety_stock": result.safety_stock,
            "reorder_point": result.reorder_point,
            "recommended_order_quantity": result.recommended_order_quantity,
            "expected_holding_cost": result.expected_holding_cost,
            "expected_shortage_risk": result.expected_shortage_risk,
            "explanation": result.explanation,
        },
        message="Inventory optimization completed",
    )


@router.post("/optimize-routes", response_model=SuccessResponse[dict], summary="Route Optimization")
def optimize_routes(
    warehouse_id: uuid.UUID = Query(...),
    order_ids: List[uuid.UUID] = Query(...),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """
    Optimize delivery routes for a set of orders from a given warehouse.
    Returns ordered stops with distance and time estimates.
    """
    ctx.require_role("system_admin", "org_admin", "operations_manager")
    org_id = ctx.resolve_org_id()
    svc = AIService(db)
    result = svc.optimize_routes(warehouse_id, order_ids, org_id)
    db.commit()
    return SuccessResponse(
        data={
            "result_id": str(result.id),
            "warehouse_id": str(warehouse_id),
            "route": result.route_data,
            "total_distance_km": result.total_distance_km,
            "estimated_duration_minutes": result.estimated_duration_minutes,
            "explanation": result.explanation,
        },
        message="Route optimization completed",
    )
