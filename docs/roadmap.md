# Roadmap

---

## v1.0 — Current Release

**Status: Complete**

All core capabilities for a working supply chain management platform are implemented, tested, and documented.

### Completed

- [x] Clean Architecture: Router → Service → Repository → Model
- [x] Cross-dialect UUID type (PostgreSQL + SQLite for testing)
- [x] 12-table PostgreSQL schema with Alembic migration (`0001_initial_schema`)
- [x] 9 ORM models: Organization, User, Warehouse, Product, InventoryItem, Order, OrderItem, plus 4 AI result models
- [x] JWT authentication with role-aware access control (5 roles)
- [x] 7 Repository classes (zero SQL in services)
- [x] 9 Service classes (all business logic)
- [x] 11 API routers: auth, users, organizations, warehouses, products, inventory, orders, AI insights, dashboard, reports, health
- [x] 4 AI modules with abstract interfaces: allocation, forecasting, optimization, routing
- [x] Frontend dashboard: 10 HTML pages, complete CSS design system, JS module architecture
- [x] Test suite: 69 tests (22 unit + 47 API), 100% pass rate
- [x] Docker + Docker Compose configuration
- [x] Alembic migrations
- [x] Seed script and setup script
- [x] Complete documentation (8 guides)

---

## v1.1 — Short-Term Improvements

These enhancements are scoped, non-breaking, and do not require architectural changes.

- [ ] **Pagination for all list endpoints** — consistent cursor-based or offset pagination
- [ ] **Activity log service** — write to `activity_logs` table on all write operations
- [ ] **User management API** — list users, update roles, deactivate users
- [ ] **Organization management API** — create/update organizations (system admin only)
- [ ] **Dashboard AI insights endpoint** — aggregate AI results for the dashboard widget
- [ ] **Reports with date filtering** — time-range parameters on report endpoints
- [ ] **Order status transition validation** — state machine enforcement in OrderService

---

## v2.0 — Platform Maturity

Larger investments that move toward production SaaS readiness.

- [ ] **Real-time notifications** — WebSocket or SSE for low-stock alerts and order status changes
- [ ] **Advanced AI models** — ARIMA/Prophet for forecasting; ML-based allocation scoring
- [ ] **Supplier management** — track suppliers, purchase orders, lead times
- [ ] **Shipment tracking** — shipment records linked to orders
- [ ] **Multi-currency and multi-unit support**
- [ ] **Audit trail UI** — browse activity_logs from the dashboard
- [ ] **API rate limiting** — per-user and per-org throttling
- [ ] **OAuth2 / SSO integration** — SAML/OIDC for enterprise identity providers
- [ ] **Background task queue** — Celery or ARQ for async AI computations
- [ ] **OpenTelemetry observability** — distributed tracing and structured metrics

---

## Design Constraints

All future changes must:

1. Maintain the Router → Service → Repository → Model layer contract
2. Keep AI modules independent of the application layer
3. Not break the existing test suite
4. Not introduce technical debt (no shortcuts, no TODOs without issues)
5. Maintain multi-tenant data isolation
