# Testing Guide

## Testing Strategy

| Type | Location | Purpose |
|------|----------|---------|
| Unit | `tests/unit/` | Test individual service and AI module functions |
| Integration | `tests/integration/` | Test repository + database interactions |
| API | `tests/api/` | Test full request/response cycle via HTTP client |

---

## Running Tests

```bash
cd backend
source .venv/bin/activate

# All tests
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=app --cov=ai --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_inventory_service.py -v

# Run specific test
pytest tests/unit/test_inventory_service.py::test_reorder_point_calculation -v

# Run only API tests
pytest tests/api/ -v
```

---

## Test Configuration

Tests use a **separate test database** configured in `conftest.py`.
The test database is created and dropped for each test session.

```bash
# Set test database URL in .env or environment
TEST_DATABASE_URL="postgresql://postgres:password@localhost:5432/supply_chain_test"
```

---

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_inventory_service.py
from backend.ai.inventory_optimization.eoq_optimizer import EOQOptimizer
from backend.ai.schemas.ai_schemas import InventoryOptimizationInput

def test_safety_stock_calculation():
    optimizer = EOQOptimizer()
    input_data = InventoryOptimizationInput(
        product_id="test-id",
        average_daily_demand=50.0,
        demand_std_dev=10.0,
        lead_time_days=5,
        service_level=0.95,
        holding_cost_per_unit=2.5,
        shortage_cost_per_unit=15.0,
    )
    result = optimizer.optimize(input_data)
    assert result.safety_stock > 0
    assert result.reorder_point >= result.safety_stock
    assert result.explanation is not None
```

### API Test Example

```python
# tests/api/test_auth.py
from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    response = await client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
```

---

## Quality Gates

Before completing any development phase:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All API tests pass
- [ ] Test coverage > 70% for new code
- [ ] No new linting errors
