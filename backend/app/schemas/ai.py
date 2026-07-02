"""AI module result schemas for API responses."""
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AllocationItemResult(BaseModel):
    product_id: uuid.UUID
    requested_quantity: float
    allocated_quantity: float
    is_fulfilled: bool


class WarehouseAllocationResponse(BaseModel):
    order_id: uuid.UUID
    warehouse_id: uuid.UUID
    warehouse_name: str
    score: float
    coverage_percentage: float
    allocation_items: List[AllocationItemResult]
    explanation: str
    saved_result_id: Optional[uuid.UUID] = None


class ForecastPoint(BaseModel):
    date: str
    predicted_quantity: float
    confidence: Optional[float] = None


class DemandForecastResponse(BaseModel):
    product_id: uuid.UUID
    product_name: str
    forecast_method: str
    horizon_days: int
    total_predicted_demand: float
    daily_forecasts: List[ForecastPoint]
    explanation: str
    saved_result_id: Optional[uuid.UUID] = None


class InventoryRecommendationResponse(BaseModel):
    product_id: uuid.UUID
    product_name: str
    warehouse_id: uuid.UUID
    warehouse_name: str
    current_stock: float
    safety_stock: float
    reorder_point: float
    recommended_order_quantity: float
    expected_holding_cost: float
    expected_shortage_risk: float
    action_required: bool
    explanation: str
    saved_result_id: Optional[uuid.UUID] = None


class RouteStop(BaseModel):
    sequence: int
    order_id: uuid.UUID
    delivery_address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class RouteOptimizationResponse(BaseModel):
    warehouse_id: uuid.UUID
    stops: List[RouteStop]
    total_distance_km: Optional[float]
    estimated_duration_minutes: Optional[int]
    explanation: str
    saved_result_id: Optional[uuid.UUID] = None
