# Environment Variables Reference

All configuration is managed through environment variables.
Copy `.env.example` to `.env` and fill in your values.
**Never commit `.env` to version control.**

---

## Application

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Supply Chain Optimization Platform` | Application display name |
| `APP_VERSION` | `1.0.0` | Current version |
| `APP_ENV` | `development` | Environment: `development`, `staging`, `production` |
| `DEBUG` | `true` | Enable debug mode (disable in production) |
| `LOG_LEVEL` | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Server

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Listen port |

## Database

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | **Yes** | PostgreSQL connection string: `postgresql://user:pass@host:port/db` |
| `DATABASE_POOL_SIZE` | `10` | Connection pool size |
| `DATABASE_MAX_OVERFLOW` | `20` | Max connections above pool size |

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | **Yes** | JWT signing key — use a long random string in production |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Access token TTL in minutes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token TTL in days |

## CORS

| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:8080` | Comma-separated allowed origins |

## Initial Seed Data

| Variable | Default | Description |
|----------|---------|-------------|
| `FIRST_ADMIN_EMAIL` | `admin@example.com` | System admin email |
| `FIRST_ADMIN_PASSWORD` | *(must set)* | System admin initial password |
| `FIRST_ADMIN_FULL_NAME` | `System Administrator` | Display name |

---

## Security Notes

- `SECRET_KEY` must be at least 32 characters in production
- `FIRST_ADMIN_PASSWORD` must be changed immediately after first login
- `DEBUG=false` must be set in production
- `DATABASE_URL` credentials must use a dedicated database user with minimal permissions
