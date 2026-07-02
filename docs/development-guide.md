# Development Guide

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend runtime |
| PostgreSQL | 15+ | Primary database |
| Git | 2.x+ | Version control |
| Docker | 24+ | Containerization (optional) |

---

## Local Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026.git
cd IBM-Bob-Challenge-2026
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY at minimum
```

### 3. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Database Setup

```bash
# Ensure PostgreSQL is running, then:
alembic upgrade head

# Seed initial data
cd ..
python scripts/seed_data.py
```

### 5. Run Development Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Development Workflow

### Branch Strategy

All development happens on `main` in this challenge context.
Each logical phase is committed independently.

### Commit Convention

```
<type>: <short description>

Types: feat, fix, refactor, test, docs, chore
Examples:
  feat: implement warehouse allocation service
  fix: correct inventory quantity validation
  docs: update API documentation
  test: add order service unit tests
```

### Adding a New Feature

1. Create/update the **Model** in `backend/app/models/`
2. Generate a **Migration**: `alembic revision --autogenerate -m "description"`
3. Create/update **Schema** in `backend/app/schemas/`
4. Implement **Repository** method in `backend/app/repositories/`
5. Implement **Service** method in `backend/app/services/`
6. Add **Router** endpoint in `backend/app/api/v1/routers/`
7. Write **Tests** in `backend/tests/`
8. Run tests: `pytest`
9. Commit

---

## Code Standards

### Python

- PEP 8 compliance
- Type hints on all function signatures
- Docstrings on all public methods
- No `print()` — use structured logging
- No secrets in code

### Layering Rules

| Layer | Can call | Cannot call |
|-------|----------|-------------|
| Router | Service, Schemas | Repository, Models directly |
| Service | Repository, AI modules | Router |
| Repository | Models, DB session | Service, Router |
| AI Module | AI schemas only | Repository, Service, Models |

### Error Handling

All errors bubble up via custom exceptions defined in `core/exceptions.py`.
Routers catch exceptions and return standardized error responses.
Never swallow exceptions silently.

---

## Database Migrations

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "add shipment table"

# Apply all pending migrations
alembic upgrade head

# Downgrade one step
alembic downgrade -1

# View migration history
alembic history
```

**Rule**: Never modify an already-applied migration. Always create a new one.

---

## Running Tests

```bash
cd backend

# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific module
pytest tests/unit/test_inventory_service.py -v

# API tests only
pytest tests/api/ -v
```

---

## Environment Variables Reference

See [environment-variables.md](environment-variables.md) for complete documentation.

---

## Adding an AI Module

1. Define input/output schema in `backend/ai/schemas/ai_schemas.py`
2. Create abstract interface in `backend/ai/interfaces/`
3. Implement algorithm in the corresponding module directory
4. Register module in the service that consumes it
5. Write unit tests
6. Document in [ai-modules.md](ai-modules.md)

The new module must NOT import from `app/` (no DB access, no service calls).
