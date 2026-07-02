# Testing Guide

## Overview

The test suite covers unit logic and full HTTP request/response cycles.
No running database is required — all tests use SQLite in-memory via the `conftest.py` fixtures.

---

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures: engine, session, client, data
├── unit/
│   ├── test_ai_modules.py   # AI algorithm logic (13 tests)
│   └── test_security.py     # JWT and password hashing (9 tests)
└── api/
    ├── test_auth_api.py      # Login, refresh, /me (8 tests)
    ├── test_health_api.py    # Health endpoint (2 tests)
    ├── test_warehouses_api.py # CRUD + deactivate (9 tests)
    ├── test_products_api.py  # CRUD (6 tests)
    ├── test_inventory_api.py # Set, get, adjust, alerts (8 tests)
    └── test_orders_api.py    # Create, get, update (8 tests)
```

**Total: 69 tests — 22 unit + 47 API**

---

## Test Infrastructure

### Database

All tests use **SQLite in-memory** via a `UUIDType` TypeDecorator that transparently handles UUID storage differences between PostgreSQL and SQLite. Each test runs in a transaction that is rolled back after the test completes — guaranteeing full isolation with no state leakage between tests.

### Fixtures (`conftest.py`)

| Fixture | Scope | Description |
|---|---|---|
| `create_tables` | session | Creates all tables once; drops after session |
| `db` | function | Transactional session; rolls back after each test |
| `client` | function | FastAPI TestClient with `get_db` overridden |
| `test_org` | function | A persisted Organization |
| `test_admin` | function | System admin User in test_org |
| `test_user` | function | Org admin User in test_org |
| `admin_headers` | function | JWT bearer headers for test_admin |
| `user_headers` | function | JWT bearer headers for test_user |
| `test_warehouse` | function | A Warehouse in test_org |
| `test_product` | function | A Product in test_org |
| `test_inventory` | function | An InventoryItem (100 units on hand) |
| `test_order` | function | An Order with one OrderItem |

---

## Running Tests

```bash
cd backend
source .venv/bin/activate

# All tests
pytest

# All tests with verbose output
pytest -v

# Unit tests only
pytest tests/unit/ -v

# API tests only
pytest tests/api/ -v

# Specific test file
pytest tests/api/test_auth_api.py -v

# Specific test class or method
pytest tests/api/test_orders_api.py::TestCreateOrder::test_create_order_success -v

# With coverage report (HTML output in htmlcov/)
pytest --cov=app --cov=ai --cov-report=html --cov-report=term-missing
```

---

## What Is Tested

### Unit Tests

- `TestMovingAverageForecaster` — forecast with data, no data, window clipping
- `TestEOQOptimizer` — basic EOQ, zero demand, reorder point formula
- `TestWarehouseAllocationEngine` — full coverage selection, no warehouses error, proximity scoring, explanation
- `TestNearestNeighborRouter` — empty stops, single stop, nearest-first ordering
- `TestPasswordHashing` — hash uniqueness, verify correct, verify wrong
- `TestJWT` — token decode, claims embedding, type claim, tampered token rejection

### API Tests

- **Auth**: login success/failure, refresh token, `/me` with and without auth
- **Health**: health endpoint response, root path
- **Warehouses**: list (auth guard, pagination), create, get by ID, update, deactivate
- **Products**: list, create, duplicate SKU conflict, get, update
- **Inventory**: list, set (create/update), get, adjust positive/negative delta, low-stock alerts
- **Orders**: list, create with items, duplicate reference conflict, get, update status

---

## Adding New Tests

1. Add a new file under `tests/api/` or `tests/unit/`
2. Import fixtures from `conftest.py` by parameter name
3. For tests requiring database objects not in fixtures, create them inline via the `db` fixture
4. Ensure each test is independent — do not rely on ordering or shared mutable state

---

## Key Design Decisions

- **No live database required** — `UUIDType` handles the PostgreSQL/SQLite dialect difference
- **Transaction rollback isolation** — each test's `db` fixture rolls back after the test
- **`lru_cache` cleared before import** — `conftest.py` calls `get_settings.cache_clear()` before importing any app module so SQLite URL is picked up
- **`get_db` dependency override** — the TestClient injects the test session, ensuring API tests hit the same in-memory DB as fixtures
