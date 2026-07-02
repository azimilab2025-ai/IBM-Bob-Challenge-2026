# API Reference

---

## Base URL

```
http://localhost:8000/api/v1
```

All responses use a consistent envelope:

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional context message"
}
```

Paginated responses use:

```json
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 42,
    "total_pages": 3
  }
}
```

Error responses:

```json
{
  "success": false,
  "error": "NOT_FOUND",
  "message": "Warehouse not found",
  "details": {}
}
```

---

## Authentication

All endpoints except `/health` and `/api/v1/auth/login` require a Bearer token:

```
Authorization: Bearer <access_token>
```

### POST `/api/v1/auth/login`

```json
// Request
{
  "email": "admin@example.com",
  "password": "YourPassword123!"
}

// Response 200
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

### POST `/api/v1/auth/refresh`

```json
// Request
{ "refresh_token": "eyJ..." }

// Response 200 — same structure as login
```

### GET `/api/v1/auth/me`

```json
// Response 200
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "admin@example.com",
    "full_name": "System Administrator",
    "role": "system_admin",
    "organization_id": "uuid"
  }
}
```

---

## Warehouses

### GET `/api/v1/warehouses`

Query params: `page` (default 1), `per_page` (default 20, max 100)

Returns active warehouses for the authenticated user's organization.

### POST `/api/v1/warehouses`

Required roles: `system_admin`, `org_admin`, `warehouse_manager`

```json
// Request
{
  "name": "East Coast DC",
  "code": "WH-EC-001",
  "city": "Boston",
  "country": "US",
  "latitude": 42.36,
  "longitude": -71.06,
  "capacity": 10000
}
```

### GET `/api/v1/warehouses/{warehouse_id}`

### PUT `/api/v1/warehouses/{warehouse_id}`

All fields optional. Same shape as POST.

### DELETE `/api/v1/warehouses/{warehouse_id}`

Soft-delete (sets `is_active=false`). Required roles: `system_admin`, `org_admin`

---

## Products

### GET `/api/v1/products`

Query params: `page`, `per_page`

### POST `/api/v1/products`

Required roles: `system_admin`, `org_admin`, `inventory_manager`

```json
{
  "name": "Widget A",
  "sku": "WGT-A-001",
  "category": "Electronics",
  "unit": "unit",
  "unit_cost": 50.0,
  "unit_price": 79.99,
  "reorder_point": 100.0,
  "lead_time_days": 14
}
```

### GET `/api/v1/products/{product_id}`

### PUT `/api/v1/products/{product_id}`

---

## Inventory

### GET `/api/v1/inventory`

Lists all inventory items across all warehouses in the organization.

### POST `/api/v1/inventory`

Creates or updates (upsert) inventory for a product/warehouse pair.

```json
{
  "product_id": "uuid",
  "warehouse_id": "uuid",
  "quantity_on_hand": 200.0,
  "reorder_point": 25.0,
  "safety_stock": 10.0
}
```

### GET `/api/v1/inventory/{item_id}`

### POST `/api/v1/inventory/{item_id}/adjust`

```json
{ "delta": 50.0 }   // positive = add, negative = remove
```

### GET `/api/v1/inventory/alerts/low-stock`

Returns all inventory items where `quantity_available <= reorder_point`.

---

## Orders

### GET `/api/v1/orders`

Query params: `page`, `per_page`, `status` (optional filter)

### POST `/api/v1/orders`

```json
{
  "reference_number": "ORD-2026-001",
  "priority": "normal",
  "delivery_address": "123 Main Street, NYC",
  "delivery_latitude": 40.71,
  "delivery_longitude": -74.01,
  "notes": "Fragile items",
  "items": [
    {
      "product_id": "uuid",
      "quantity": 10.0,
      "unit_price": 79.99
    }
  ]
}
```

### GET `/api/v1/orders/{order_id}`

### PATCH `/api/v1/orders/{order_id}`

```json
{ "status": "confirmed" }
```

Valid statuses: `pending` → `confirmed` → `allocated` → `in_progress` → `shipped` → `delivered` | `cancelled`

### POST `/api/v1/orders/{order_id}/allocate`

Triggers AI warehouse allocation. Required roles: `system_admin`, `org_admin`, `operations_manager`

```json
// Response
{
  "success": true,
  "data": {
    "result_id": "uuid",
    "order_id": "uuid",
    "warehouse_id": "uuid",
    "score": 0.87,
    "coverage_percentage": 100.0,
    "explanation": "Warehouse WH-EC-001 selected: 100% inventory coverage, proximity score 0.91."
  }
}
```

---

## AI Insights

### GET `/api/v1/ai/forecast/{product_id}`

Returns demand forecast for the given product.

### GET `/api/v1/ai/optimize/{product_id}`

Returns inventory optimization recommendation (EOQ, safety stock, reorder point).

---

## Dashboard

### GET `/api/v1/dashboard/summary`

Returns aggregate KPIs:
- Total orders (by status)
- Low-stock item count
- Active warehouses
- Recent order activity

---

## Reports

### GET `/api/v1/reports/inventory`

Returns inventory summary per product and warehouse.

---

## System

### GET `/health`

Unauthenticated. Returns `{"status": "ok", "version": "1.0.0"}`.

---

## Error Codes

| HTTP | Error Code | Meaning |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Invalid input data |
| 401 | `AUTHENTICATION_ERROR` | Missing or invalid token |
| 403 | `AUTHORIZATION_ERROR` | Insufficient role |
| 404 | `NOT_FOUND` | Resource does not exist |
| 409 | `CONFLICT_ERROR` | Duplicate resource (e.g., same SKU) |
| 422 | — | Pydantic validation failure (automatic) |
| 500 | `INTERNAL_ERROR` | Unexpected server error |
