# Architecture Overview

---

## Design Principles

1. **Clean Architecture** — strict one-way dependency: Router → Service → Repository → Model
2. **Independent AI Modules** — AI services are pluggable, isolated, and testable without the rest of the application
3. **SaaS Readiness** — multi-tenant from day one (every record belongs to an Organization)
4. **Security by Design** — authentication and authorization enforced at the dependency injection layer
5. **No Business Logic in Routers** — routers only validate input, call a service, and serialize output

---

## System Layers

```
HTTP Request
     │
     ▼
┌─────────────────────────────────────────────┐
│              Routers (app/api/)              │
│  - Validate request (Pydantic)              │
│  - Enforce authentication (JWT dependency)  │
│  - Call exactly one Service method          │
│  - Serialize response (Pydantic)            │
│  - NO if/else business rules                │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│              Services (app/services/)          │
│  - All business logic lives here              │
│  - Validate domain rules                      │
│  - Orchestrate repositories                   │
│  - Call AI modules when needed                │
│  - Control transactions (commit/rollback)     │
└───────────────┬───────────────┬───────────────┘
                │               │
                ▼               ▼
┌───────────────────┐  ┌──────────────────────┐
│   Repositories    │  │     AI Modules        │
│  (app/repos/)     │  │     (ai/)             │
│  - SQL queries    │  │  - Pluggable impls    │
│  - No logic       │  │  - Isolated, testable │
└────────┬──────────┘  └──────────────────────┘
         │
         ▼
┌─────────────────────┐
│   ORM Models        │
│  (app/models/)      │
│  - Table definitions│
│  - Computed props   │
│  - No business logic│
└─────────────────────┘
```

---

## Multi-Tenancy

Every domain entity (Warehouse, Product, InventoryItem, Order) is scoped to an `Organization`. The `CurrentUserContext` dependency resolves the calling user's organization from the JWT token and injects it into every service call. A user can never access data from another organization.

```python
# Every protected route resolves org_id from the authenticated token
org_id = ctx.resolve_org_id()
warehouses = svc.list_by_org(org_id, ...)
```

---

## Authentication & Authorization

- **JWT tokens** (HS256) are issued on login and carry `sub` (user ID), `role`, and `org_id` claims
- **`get_current_user_id`** dependency — validates JWT and extracts user ID
- **`get_current_user_context`** dependency — full context: user UUID, role, org_id
- **`ctx.require_role(...)`** — raises `AuthorizationError` if the caller's role is not in the allowed set
- Role checks happen in routers, not in services

---

## Database Schema

12 tables across 4 domains:

```
organizations
    ├── users
    ├── warehouses
    │       └── inventory_items ──────── products
    │                                        │
    └── orders ─────────────── order_items ──┘
            │
            └── warehouse_allocation_results

demand_forecasts
inventory_recommendations
route_optimization_results
activity_logs
```

All primary keys and foreign keys use `UUIDType` — a cross-dialect TypeDecorator that stores native UUIDs on PostgreSQL and CHAR(36) on SQLite, exposing `uuid.UUID` objects to application code in both cases.

---

## AI Module Architecture

Each AI module implements a defined abstract interface:

```
ai/
├── interfaces/
│   ├── demand_forecaster.py     # DemandForecasterInterface
│   ├── inventory_optimizer.py   # InventoryOptimizerInterface
│   ├── warehouse_allocator.py   # WarehouseAllocatorInterface
│   └── route_optimizer.py       # RouteOptimizerInterface
├── demand_forecasting/
│   └── moving_average.py        # MovingAverageForecaster(DemandForecasterInterface)
├── inventory_optimization/
│   └── eoq_optimizer.py         # EOQOptimizer(InventoryOptimizerInterface)
├── warehouse_allocation/
│   └── allocation_engine.py     # AllocationEngine(WarehouseAllocatorInterface)
└── route_optimization/
    └── basic_router.py          # NearestNeighborRouter(RouteOptimizerInterface)
```

Services instantiate the concrete implementation. To swap the algorithm, change one line in the service — no other code changes required.

---

## Request Flow Example: Create Order

```
POST /api/v1/orders
     │
     ▼ OrdersRouter.create_order()
         - Validates OrderCreate schema
         - Calls ctx.resolve_org_id()
         │
         ▼ OrderService.create(org_id, user_id, data)
             - Checks reference_number uniqueness (via OrderRepository)
             - Creates Order + OrderItems
             - Returns Order ORM object
         │
         ▼ Router commits transaction, refreshes, serializes OrderResponse
         │
         ▼ HTTP 201 response
```

```
POST /api/v1/orders/{id}/allocate
     │
     ▼ OrdersRouter.allocate_order()
         │
         ▼ AIService.allocate_order(order_id, org_id)
             - Loads Order (via OrderRepository)
             - Loads active Warehouses (via WarehouseRepository)
             - Loads Inventory (via InventoryRepository)
             - Calls AllocationEngine.allocate(order, warehouses, inventory)
             - Persists WarehouseAllocationResult
             - Returns result
         │
         ▼ HTTP 200 with allocation details + explanation
```

---

## Error Handling

All domain errors map to HTTP status codes via exception handlers registered in `main.py`:

| Exception | HTTP Status |
|---|---|
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `ValidationError` | 400 |
| `AuthenticationError` | 401 |
| `AuthorizationError` | 403 |
| `AppException` | 500 |

No raw exceptions leak to the HTTP layer.

---

## Cross-Dialect UUID

`app/db/types.py` defines `UUIDType`, a `TypeDecorator` that:
- On PostgreSQL: delegates to native `UUID(as_uuid=True)` — optimal storage and indexing
- On SQLite (tests): stores as `CHAR(36)` hyphenated string
- Both sides: coerce to/from `uuid.UUID` transparently

This ensures the production schema uses native PostgreSQL UUID columns, while the test suite runs without any database infrastructure.
