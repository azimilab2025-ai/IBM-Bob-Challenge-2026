# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/auth/login` and `/health`) require a Bearer token:

```
Authorization: Bearer <access_token>
```

---

## Standard Response Format

### Success

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}
```

### Error

```json
{
  "success": false,
  "error": "RESOURCE_NOT_FOUND",
  "message": "Warehouse with id 42 not found",
  "details": {}
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (delete) |
| 400 | Bad Request / Validation Error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

---

## Endpoints Summary

### Authentication
- `POST /auth/login` — Obtain access token
- `POST /auth/refresh` — Refresh access token
- `POST /auth/logout` — Revoke token
- `GET /auth/me` — Current user profile

### Users
- `GET /users` — List users (admin)
- `POST /users` — Create user
- `GET /users/{id}` — Get user
- `PUT /users/{id}` — Update user
- `DELETE /users/{id}` — Deactivate user

### Organizations
- `GET /organizations` — List organizations
- `POST /organizations` — Create organization
- `GET /organizations/{id}` — Get organization
- `PUT /organizations/{id}` — Update organization

### Warehouses
- `GET /warehouses` — List warehouses (org-scoped)
- `POST /warehouses` — Create warehouse
- `GET /warehouses/{id}` — Get warehouse
- `PUT /warehouses/{id}` — Update warehouse
- `DELETE /warehouses/{id}` — Deactivate warehouse

### Products
- `GET /products` — List products (org-scoped)
- `POST /products` — Create product
- `GET /products/{id}` — Get product
- `PUT /products/{id}` — Update product

### Inventory
- `GET /inventory` — List inventory items
- `POST /inventory` — Add inventory record
- `PUT /inventory/{id}` — Update inventory quantity
- `GET /inventory/alerts` — Low stock alerts

### Orders
- `GET /orders` — List orders (org-scoped, paginated)
- `POST /orders` — Create order with items
- `GET /orders/{id}` — Get order details
- `PUT /orders/{id}/status` — Update order status
- `POST /orders/{id}/allocate` — Trigger warehouse allocation

### AI Insights
- `POST /ai/forecast` — Demand forecast for a product
- `POST /ai/optimize-inventory` — Inventory optimization recommendations
- `POST /ai/allocate-warehouse` — Warehouse allocation for an order
- `POST /ai/optimize-route` — Route optimization for deliveries

### Dashboard
- `GET /dashboard/summary` — KPIs and operational overview
- `GET /dashboard/alerts` — Active operational alerts

### Reports
- `GET /reports/inventory` — Inventory status report
- `GET /reports/orders` — Order activity report
- `GET /reports/forecasts` — Forecast accuracy report

### System
- `GET /health` — Health check (no auth required)
- `GET /settings` — System settings (admin)

---

## Interactive Docs

When the server is running:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
