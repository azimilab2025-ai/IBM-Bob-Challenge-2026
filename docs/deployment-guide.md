# Deployment Guide

## Local Development

See [Development Guide](development-guide.md) for local setup.

---

## Docker Deployment

### Prerequisites
- Docker 24+
- Docker Compose v2+

### Quick Start

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with production values

# 2. Start all services
docker-compose up -d

# 3. Run database migrations
docker-compose exec backend alembic upgrade head

# 4. Seed initial data
docker-compose exec backend python /app/scripts/seed_data.py

# 5. Verify health
curl http://localhost:8000/health
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| `backend` | 8000 | FastAPI application |
| `postgres` | 5432 | PostgreSQL database |
| `frontend` | 8080 | Static file server (nginx) |

---

## Environment Configuration for Production

Critical settings to change from defaults:

```env
APP_ENV=production
DEBUG=false
SECRET_KEY=<minimum-32-character-random-string>
DATABASE_URL=postgresql://appuser:strongpassword@db:5432/supply_chain_prod
FIRST_ADMIN_PASSWORD=<strong-initial-password>
CORS_ORIGINS=https://yourdomain.com
```

---

## Health Check

```
GET /health

Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

---

## Logs

Application logs are written to stdout in structured JSON format.
Collect with your preferred log aggregator (CloudWatch, Datadog, ELK).

Log level is controlled by `LOG_LEVEL` environment variable.
