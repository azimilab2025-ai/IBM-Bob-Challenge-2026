# Architecture Overview

## Design Principles

This system is built on five core engineering principles:

1. **Layered Architecture** — strict separation between Router, Service, Repository, and Model layers
2. **Independent AI Modules** — AI services are pluggable and testable in isolation
3. **SaaS Readiness** — multi-tenant architecture from day one
4. **Security by Design** — authentication and authorization are not afterthoughts
5. **Extensibility** — every interface is designed for future replacement without breaking changes

---

## System Layers

```
┌─────────────────────────────────────────────┐
│              HTTP Request                    │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│           API Layer (Routers)                │
│  - Request validation                        │
│  - Response serialization                   │
│  - Authentication middleware                 │
│  - NO business logic                        │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│          Service Layer                       │
│  - All business logic lives here            │
│  - Orchestrates repositories and AI         │
│  - Domain validation and rules              │
│  - Transaction management                   │
└──────────┬────────────────┬─────────────────┘
           │                │
┌──────────▼──────┐  ┌──────▼──────────────────┐
│ Repository Layer│  │      AI Modules          │
│ - DB queries    │  │ - Demand Forecasting     │
│ - CRUD only     │  │ - Warehouse Allocation   │
│ - No logic      │  │ - Inventory Optimization │
└──────────┬──────┘  │ - Route Optimization     │
           │         └──────────────────────────┘
┌──────────▼──────────────────────────────────┐
│              Database (PostgreSQL)           │
│  - SQLAlchemy ORM models                    │
│  - Alembic migrations                       │
└─────────────────────────────────────────────┘
```

---

## Module Map

| Module | Path | Responsibility |
|--------|------|----------------|
| `core/config.py` | Settings management | Environment variables, app configuration |
| `core/security.py` | Auth utilities | JWT encoding/decoding, password hashing |
| `core/dependencies.py` | FastAPI deps | Current user injection, DB session |
| `core/logging.py` | Structured logging | Centralized log configuration |
| `db/session.py` | DB session | SQLAlchemy session factory |
| `db/base.py` | Base model | Declarative base, common columns |
| `models/` | ORM models | SQLAlchemy table definitions |
| `schemas/` | Pydantic schemas | Request/response contracts |
| `repositories/` | Data access | All database queries |
| `services/` | Business logic | All domain operations |
| `api/v1/routers/` | HTTP handlers | Route definitions only |
| `ai/interfaces/` | AI contracts | Abstract base classes |
| `ai/*/` | AI implementations | Pluggable algorithm modules |

---

## Data Flow: Order Allocation

```
POST /api/v1/orders/{id}/allocate
         │
         ▼
    OrderRouter
    (validate request, check auth)
         │
         ▼
    OrderService
    (orchestrate allocation workflow)
         │
    ┌────┴──────────────────────────────┐
    │                                   │
    ▼                                   ▼
InventoryRepository          WarehouseAllocationEngine
(fetch stock levels)         (score and rank warehouses)
    │                                   │
    └────────────────┬──────────────────┘
                     ▼
              AllocationResult
              (with explanation)
                     │
                     ▼
         WarehouseAllocationResult
              (persisted to DB)
                     │
                     ▼
              JSON Response
```

---

## Multi-Tenant Design

Each organization operates in complete data isolation:

- Every major entity has an `organization_id` foreign key
- All repository queries are scoped by `organization_id`
- Users are bound to exactly one organization (except `system_admin`)
- System Admin operates across all organizations

This design supports future SaaS evolution without requiring a schema redesign.

---

## AI Module Architecture

```
┌─────────────────────────────────────┐
│         Abstract Interface          │
│  (e.g., BaseForecaster)             │
│  - defines input/output contract    │
│  - enforces predict() signature     │
└────────────────┬────────────────────┘
                 │  implements
    ┌────────────┴────────────────┐
    │                             │
┌───▼──────────────┐   ┌─────────▼──────────────┐
│ MovingAverage    │   │ FutureMLModel           │
│ Forecaster (v1)  │   │ (plug in without        │
│                  │   │  touching business logic)│
└──────────────────┘   └────────────────────────┘
```

All AI modules:
- Accept a well-defined input schema
- Return a well-defined output schema including `explanation`
- Have zero dependency on the database
- Are independently testable

---

## Security Architecture

- **Secrets**: all from environment variables, never in source code
- **Passwords**: bcrypt hashed, never stored or logged as plaintext
- **JWT**: centralized in `core/security.py`, validated per-request via dependency
- **Authorization**: role-based, enforced at service layer
- **Input validation**: Pydantic schemas on every endpoint
- **Principle of Least Privilege**: each role can only access what it needs

---

## Database Design Principles

- **PostgreSQL** as the only supported database
- **Alembic** for all schema changes — no `create_all` in production
- **Soft deletes** where appropriate (is_active flag)
- **Audit columns** on all major tables: `created_at`, `updated_at`, `created_by`
- **Foreign keys and indexes** explicitly defined
- **No raw SQL** in application code — SQLAlchemy ORM only

---

## API Design Contract

- **Versioned**: `/api/v1/`
- **RESTful**: standard HTTP methods and status codes
- **Consistent response envelope**:
  ```json
  {
    "success": true,
    "data": {...},
    "message": "Operation completed",
    "meta": {"page": 1, "total": 100}
  }
  ```
- **Error response**:
  ```json
  {
    "success": false,
    "error": "RESOURCE_NOT_FOUND",
    "message": "Warehouse with id 42 not found",
    "details": {}
  }
  ```
- **Pagination** on all list endpoints
- **OpenAPI** auto-generated via FastAPI
