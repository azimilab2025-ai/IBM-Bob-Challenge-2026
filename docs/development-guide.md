# Development Guide

---

## Prerequisites

| Tool | Minimum Version |
|---|---|
| Python | 3.9 |
| PostgreSQL | 15 (or use Docker) |
| Git | 2.x |

---

## Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026.git
cd IBM-Bob-Challenge-2026

# 2. Configure environment
cp .env.example .env
# Edit .env — at minimum set DATABASE_URL and SECRET_KEY

# 3. Create virtual environment
cd backend
python3 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 4. Install production and development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. Run database migrations
alembic upgrade head

# 6. Seed initial data (first run only)
python ../scripts/seed_data.py

# 7. Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/supplychain
SECRET_KEY=your-secret-key-at-least-32-chars-long
APP_ENV=development
DEBUG=true
```

See [Environment Variables](environment-variables.md) for a full reference.

---

## Running Tests

```bash
# All tests (no database required — uses SQLite in-memory)
pytest -v

# Specific subset
pytest tests/unit/ -v
pytest tests/api/ -v

# With coverage
pytest --cov=app --cov=ai --cov-report=term-missing
```

The test suite requires no live database. See [Testing Guide](testing-guide.md) for details.

---

## Database Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Check current state
alembic current

# View migration history
alembic history

# Create a new migration (after changing models)
alembic revision --autogenerate -m "describe_your_change"

# Downgrade one step
alembic downgrade -1
```

---

## Code Organization

```
backend/app/
├── api/v1/routers/   → One file per resource. Only routing + serialization.
├── core/             → Config, security, exceptions, logging, dependencies.
├── db/               → Base declarative, UUIDType, session factory.
├── models/           → SQLAlchemy ORM models. Computed properties allowed.
├── schemas/          → Pydantic schemas. Separate Create/Update/Response per resource.
├── repositories/     → All SQL queries. No business logic. Return ORM objects.
└── services/         → All business logic. Orchestrate repos + AI. Control transactions.
```

**Non-negotiable rules:**
- Routers never contain `if` business logic
- Services never write SQL directly — use repositories
- Repositories never import services
- AI modules never import from `app/`

---

## Adding a New Resource

1. Add the ORM model to `app/models/` — inherit from `Base, BaseModel`
2. Add migration: `alembic revision --autogenerate -m "add_<resource>"`
3. Add Pydantic schemas to `app/schemas/`
4. Add a repository to `app/repositories/` inheriting from `BaseRepository`
5. Add a service to `app/services/` — inject the repository
6. Add a router to `app/api/v1/routers/` — register in `main.py`
7. Add tests to `tests/api/test_<resource>_api.py`

---

## Commit Message Convention

```
<type>(<scope>): <short description>

Types: feat, fix, refactor, test, docs, chore
Scope: phase-N, auth, inventory, ai, etc.

Examples:
feat(inventory): add low-stock alert endpoint
fix(auth): correct token expiry calculation
test(api): add warehouse deactivation test
docs(readme): update v1 status checklist
```

---

## Project Conventions

| Convention | Rule |
|---|---|
| Language | All code, comments, variables, and docs in English |
| UUID | Always use `UUIDType` from `app.db.types` — never `postgresql.UUID` directly |
| Error handling | Always raise a domain exception (`NotFoundError`, etc.) — never return None silently |
| Transactions | Services own transactions — routers call `db.commit()` after service returns |
| Secrets | Never hardcode secrets — always use `get_settings()` |
| Imports | Avoid circular imports — use `TYPE_CHECKING` for type hints between models |
