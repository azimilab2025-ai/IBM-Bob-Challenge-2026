# AI Modules

---

## Design Philosophy

All AI modules in this platform are:

1. **Independent** — no imports from `app/` layer; zero knowledge of HTTP or ORM
2. **Pluggable** — each module implements a defined abstract interface
3. **Explainable** — every result includes a human-readable explanation
4. **Testable in isolation** — unit tests require no database or HTTP infrastructure

To swap an algorithm, change the concrete class in the service — no other code changes required.

---

## Module Overview

| Module | Interface | Implementation | Algorithm |
|---|---|---|---|
| Warehouse Allocation | `WarehouseAllocatorInterface` | `AllocationEngine` | Score-based: availability × capacity × proximity |
| Demand Forecasting | `DemandForecasterInterface` | `MovingAverageForecaster` | Simple / weighted moving average |
| Inventory Optimization | `InventoryOptimizerInterface` | `EOQOptimizer` | Economic Order Quantity + safety stock |
| Route Optimization | `RouteOptimizerInterface` | `NearestNeighborRouter` | Nearest-neighbor greedy algorithm |

---

## Warehouse Allocation Engine

**File:** `ai/warehouse_allocation/allocation_engine.py`

**Problem:** Given an order with multiple product items, which warehouse should fulfill it?

**Algorithm:**
1. For each active warehouse, compute a composite score:
   - **Availability score** (0–1): what fraction of ordered quantities are available in this warehouse?
   - **Capacity score** (0–1): current utilization relative to warehouse capacity
   - **Proximity score** (0–1): inverse normalized haversine distance from delivery address
2. Weighted sum: `score = 0.5 × availability + 0.3 × capacity + 0.2 × proximity`
3. Select the highest-scoring warehouse

**Output includes:**
- Selected `warehouse_id`
- Composite `score`
- `coverage_percentage` — percentage of order items that can be fulfilled
- `explanation` — human-readable rationale

**Extensibility:** Replace `AllocationEngine` with a model that uses historical fulfillment data, SLA constraints, or cost optimization.

---

## Demand Forecasting

**File:** `ai/demand_forecasting/moving_average.py`

**Problem:** Given historical demand data for a product, forecast future demand.

**Algorithm:**
- Simple moving average over the last `window_size` periods (default: 7)
- Window is clamped to the available data length
- If no historical data is available, returns zero forecast with a low-confidence flag

**Output includes:**
- `forecast_values` — list of predicted demand values per period
- `method` — algorithm identifier
- `confidence` — estimate based on data variance
- `explanation` — human-readable description

**Extensibility:** Replace with ARIMA, Facebook Prophet, or an LSTM model by implementing `DemandForecasterInterface`.

---

## Inventory Optimizer (EOQ)

**File:** `ai/inventory_optimization/eoq_optimizer.py`

**Problem:** Given a product's demand and costs, what is the optimal order quantity and reorder point?

**Algorithm:**
- **Economic Order Quantity (EOQ):** `EOQ = sqrt(2 × D × S / H)` where:
  - D = annual demand
  - S = order cost (setup/ordering cost)
  - H = annual holding cost per unit
- **Safety Stock:** `safety_stock = z × σ_d × sqrt(L)` where:
  - z = service level z-score (lookup table, no scipy dependency)
  - σ_d = demand standard deviation
  - L = lead time in days
- **Reorder Point:** `ROP = (daily_demand × lead_time) + safety_stock`

**Output includes:**
- `recommended_order_quantity` (EOQ)
- `safety_stock`
- `reorder_point`
- `expected_holding_cost`
- `expected_shortage_risk`
- `explanation`

**Extensibility:** Replace with stochastic or simulation-based optimization by implementing `InventoryOptimizerInterface`.

---

## Route Optimizer

**File:** `ai/route_optimization/basic_router.py`

**Problem:** Given a depot and a list of delivery stops, find an efficient route.

**Algorithm:**
- Nearest-neighbor greedy heuristic
- Starting from the depot, always move to the closest unvisited stop (haversine distance)
- Returns the ordered stop sequence, total distance, and estimated duration

**Output includes:**
- `route` — ordered list of stop coordinates and labels
- `total_distance_km`
- `estimated_duration_minutes`
- `explanation`

**Extensibility:** Replace with Clarke-Wright savings, simulated annealing, or a VRP solver by implementing `RouteOptimizerInterface`.

---

## Interfaces

All interfaces are defined in `ai/interfaces/`:

```python
class WarehouseAllocatorInterface(ABC):
    @abstractmethod
    def allocate(self, order: AllocationRequest, warehouses: List[WarehouseOption]) -> AllocationResult:
        ...

class DemandForecasterInterface(ABC):
    @abstractmethod
    def forecast(self, request: ForecastRequest) -> ForecastResult:
        ...

class InventoryOptimizerInterface(ABC):
    @abstractmethod
    def optimize(self, request: OptimizationRequest) -> OptimizationResult:
        ...

class RouteOptimizerInterface(ABC):
    @abstractmethod
    def optimize_route(self, request: RouteRequest) -> RouteResult:
        ...
```

AI schemas (input/output data classes) are defined in `ai/schemas/ai_schemas.py` — fully decoupled from ORM models.
