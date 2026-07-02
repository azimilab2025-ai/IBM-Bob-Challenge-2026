# Deployment Guide

---

## Prerequisites

- Docker 24+ and Docker Compose v2+
- Or: Python 3.9+, PostgreSQL 15+

---

## Local Development (Without Docker)

```bash
# Clone the repository
git clone https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026.git
cd IBM-Bob-Challenge-2026

# Configure environment
cp .env.example .env
# Edit .env — required values: DATABASE_URL, SECRET_KEY

# Set up the backend
cd backend
python3 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed initial admin user and sample data
python ../scripts/seed_data.py

# Start the development server (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access points:**
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Frontend: open `frontend/index.html` directly, or serve it with any static file server

---

## Docker Deployment

### Quick Start

```bash
# 1. Configure environment
cp .env.example .env
# Set production DATABASE_URL, SECRET_KEY, etc.

# 2. Start all services
docker-compose up -d

# 3. Run database migrations
docker-compose exec backend alembic upgrade head

# 4. Seed initial data (first deployment only)
docker-compose exec backend python /app/scripts/seed_data.py

# 5. Verify health
curl http://localhost:8000/health
```

### Services

| Service | Port | Description |
|---|---|---|
| `backend` | 8000 | FastAPI application |
| `postgres` | 5432 | PostgreSQL 15 database |

### Stopping Services

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (WARNING: deletes database)
docker-compose down -v
```

---

## Production Considerations

### Environment Variables

All secrets and environment-specific config must be in `.env`. Never commit `.env` to version control. See [Environment Variables](environment-variables.md) for a full list.

**Required for production:**

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<at least 32 characters, cryptographically random>
APP_ENV=production
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
```

Generate a strong secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

### Security Checklist

- [ ] `SECRET_KEY` is at least 32 characters and randomly generated
- [ ] `APP_ENV=production` is set
- [ ] `DEBUG=false` is set
- [ ] `CORS_ORIGINS` is restricted to your domain
- [ ] PostgreSQL is not exposed to the public internet
- [ ] Admin credentials are changed from defaults
- [ ] HTTPS is terminated at the load balancer or reverse proxy

### Database Migrations

Always run migrations before starting the application on a new deployment:

```bash
alembic upgrade head
```

To check current migration state:

```bash
alembic current
alembic history
```

### Scaling

The FastAPI application is stateless — it can be scaled horizontally behind a load balancer. The only shared state is the PostgreSQL database, which should be provisioned with connection pooling (e.g., PgBouncer) for high-traffic scenarios.

---

## One-Command Local Setup

A convenience script is provided:

```bash
cd IBM-Bob-Challenge-2026
bash scripts/setup.sh
```

This script installs dependencies, creates `.env` from `.env.example` if it does not exist, runs migrations, and seeds sample data.

---

## Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok", "version": "1.0.0"}
```

The `/health` endpoint is unauthenticated and suitable for use with Docker health checks, load balancer probes, and uptime monitors.
