"""
Input/Output schemas for all AI modules.
These schemas are independent of the application models and DB layer.
AI modules must only use these schemas — never import from app/.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Demand Forecasting
# ---------------------------------------------------------------------------

@dataclass
class HistoricalDataPoint:
    date: str          # ISO 8601 date string e.g. "2025-01-15"
    quantity: float


@dataclass
class ForecastInput:
    product_id: str
    historical_data: List[HistoricalDataPoint]
    horizon_days: int = 30
    window_size: int = 7


@dataclass
class ForecastPoint:
    date: str
    predicted_quantity: float
    confidence: Optional[float] = None


@dataclass
class ForecastOutput:
    product_id: str
    method: str
    horizon_days: int
    daily_forecasts: List[ForecastPoint]
    total_predicted_demand: float
    explanation: str


# ---------------------------------------------------------------------------
# Warehouse Allocation
# ---------------------------------------------------------------------------

@dataclass
class OrderItemInput:
    product_id: str
    quantity: float


@dataclass
class WarehouseStockInput:
    warehouse_id: str
    warehouse_name: str
    latitude: Optional[float]
    longitude: Optional[float]
    capacity: Optional[int]
    stock_by_product: Dict[str, float] = field(default_factory=dict)  # product_id -> available qty


@dataclass
class AllocationRequest:
    order_id: str
    delivery_latitude: Optional[float]
    delivery_longitude: Optional[float]
    items: List[OrderItemInput]
    warehouses: List[WarehouseStockInput]


@dataclass
class AllocationItemResult:
    product_id: str
    requested_quantity: float
    allocated_quantity: float
    is_fulfilled: bool


@dataclass
class AllocationOutput:
    order_id: str
    warehouse_id: str
    warehouse_name: str
    score: float
    coverage_percentage: float
    items: List[AllocationItemResult]
    explanation: str


# ---------------------------------------------------------------------------
# Inventory Optimization
# ---------------------------------------------------------------------------

@dataclass
class InventoryOptimizationInput:
    product_id: str
    warehouse_id: str
    average_daily_demand: float
    demand_std_dev: float
    lead_time_days: float
    service_level: float = 0.95         # 0.0 – 1.0
    holding_cost_per_unit: float = 1.0
    shortage_cost_per_unit: float = 10.0
    annual_order_cost: float = 50.0


@dataclass
class InventoryOptimizationOutput:
    product_id: str
    warehouse_id: str
    safety_stock: float
    reorder_point: float
    recommended_order_quantity: float
    expected_holding_cost: float
    expected_shortage_risk: float
    explanation: str


# ---------------------------------------------------------------------------
# Route Optimization
# ---------------------------------------------------------------------------

@dataclass
class DeliveryStop:
    order_id: str
    delivery_address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


@dataclass
class RouteInput:
    warehouse_id: str
    warehouse_latitude: Optional[float]
    warehouse_longitude: Optional[float]
    stops: List[DeliveryStop]


@dataclass
class RouteStop:
    sequence: int
    order_id: str
    delivery_address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


@dataclass
class RouteOutput:
    warehouse_id: str
    stops: List[RouteStop]
    total_distance_km: Optional[float]
    estimated_duration_minutes: Optional[int]
    explanation: str
