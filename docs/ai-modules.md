# AI Modules Overview

## Design Principles

All AI modules follow these rules:
1. **Zero database access** — modules receive data as input, return results as output
2. **Pluggable via interface** — swap algorithms without touching business logic
3. **Explainable outputs** — every result includes a human-readable reasoning field
4. **Independent testability** — each module is unit-testable with mock data

---

## Module 1: Warehouse Allocation Engine

**Purpose**: Given an order, determine the optimal warehouse(s) to fulfill it.

**Input**: Order items with quantities, list of warehouses with current inventory

**Algorithm (v1)**: Weighted scoring based on:
- Available stock coverage (primary factor)
- Warehouse capacity utilization
- Distance/priority score

**Output**:
```json
{
  "order_id": "uuid",
  "allocations": [
    {
      "warehouse_id": "uuid",
      "warehouse_name": "Central Warehouse",
      "items_covered": [...],
      "coverage_percentage": 95.0,
      "score": 0.87,
      "explanation": "Selected based on 95% stock coverage and low utilization"
    }
  ],
  "unallocated_items": []
}
```

**Extension path**: Add cost matrix, time windows, vehicle constraints → Full VRP

---

## Module 2: Demand Forecasting

**Purpose**: Predict future demand for a product based on historical data.

**Input**: Historical sales/order data (time series), forecast horizon

**Algorithm (v1)**: Simple Moving Average over configurable window

**Output**:
```json
{
  "product_id": "uuid",
  "forecast_periods": 30,
  "predicted_demand": [
    {"date": "2025-02-01", "quantity": 42.5, "confidence": 0.75}
  ],
  "method": "moving_average",
  "window_size": 7,
  "explanation": "Based on 7-day moving average of last 30 days of order data"
}
```

**Extension path**: ARIMA → Prophet → LSTM without interface changes

---

## Module 3: Inventory Optimization

**Purpose**: Calculate optimal inventory levels to minimize cost while maintaining service level.

**Input**: Historical demand data, lead time, holding cost, shortage cost, service level target

**Algorithm (v1)**: Economic Order Quantity (EOQ) with safety stock calculation

**Output**:
```json
{
  "product_id": "uuid",
  "warehouse_id": "uuid",
  "safety_stock": 150,
  "reorder_point": 280,
  "recommended_order_quantity": 500,
  "expected_holding_cost": 1250.00,
  "expected_shortage_risk": 0.05,
  "explanation": "EOQ calculated at 500 units based on annual demand 6000, holding cost $2.50/unit/year"
}
```

**Extension path**: Stochastic demand models, multi-echelon optimization

---

## Module 4: Route Optimization

**Purpose**: Determine an efficient delivery sequence for a set of orders.

**Input**: List of delivery locations with coordinates, warehouse origin

**Algorithm (v1)**: Nearest neighbor heuristic

**Output**:
```json
{
  "route_id": "uuid",
  "stops": [
    {"order_id": "uuid", "sequence": 1, "location": {...}, "estimated_arrival": "..."}
  ],
  "total_distance_km": 125.4,
  "estimated_duration_minutes": 180,
  "explanation": "Nearest-neighbor route minimizing total travel distance"
}
```

**Extension path**: 2-opt improvement → Christofides → VRP with capacity constraints

---

## Interface Contract

Every AI module implements its base interface:

```python
class BaseForecaster(ABC):
    @abstractmethod
    def predict(self, input_data: ForecastInput) -> ForecastOutput:
        """Generate demand forecast."""
        ...
```

Services call modules only through these interfaces. This ensures:
- New algorithms can be added without modifying service code
- Modules can be tested with mock implementations
- A/B testing between algorithm versions is straightforward
