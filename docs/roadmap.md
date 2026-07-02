# Project Roadmap

## Version 1.0 — MVP (Current)

Target: Complete, runnable, demo-ready platform covering the core supply chain workflow.

### Phase 0 — Repository & Documentation
- [x] Repository structure
- [x] Architecture documentation
- [x] Development guide
- [x] Environment configuration

### Phase 1 — Configuration & Database
- [ ] Application configuration (Pydantic Settings)
- [ ] Database session and base model
- [ ] Alembic setup

### Phase 2 — Models & Schemas
- [ ] User, Role, Organization models
- [ ] Warehouse, Product, InventoryItem models
- [ ] Order, OrderItem models
- [ ] AI result models (allocation, forecast, optimization)
- [ ] ActivityLog, SystemSetting models
- [ ] All Pydantic schemas

### Phase 3 — Authentication
- [ ] JWT token generation and validation
- [ ] Password hashing
- [ ] Login / refresh token endpoints
- [ ] Current user dependency

### Phase 4 — Core Business Modules
- [ ] Organization management
- [ ] User management with role assignment
- [ ] Warehouse management
- [ ] Product management
- [ ] Inventory management
- [ ] Order management

### Phase 5 — AI Modules
- [ ] Warehouse Allocation Engine
- [ ] Demand Forecasting (Moving Average)
- [ ] Inventory Optimization (EOQ)
- [ ] Route Optimization (Basic)

### Phase 6 — Dashboard & Frontend
- [ ] Login page
- [ ] Main dashboard with KPIs
- [ ] Warehouses page
- [ ] Products page
- [ ] Inventory page
- [ ] Orders page
- [ ] AI Insights page
- [ ] Reports page
- [ ] Settings page

### Phase 7 — Testing
- [ ] Unit tests for all services
- [ ] Unit tests for AI modules
- [ ] Integration tests for repositories
- [ ] API endpoint tests

### Phase 8 — Deployment
- [ ] Dockerfile for backend
- [ ] Docker Compose (backend + PostgreSQL + frontend)
- [ ] Health check endpoint
- [ ] Production environment configuration

---

## Version 2.0 — SaaS Evolution (Future)

- Multi-tenant billing and subscription management
- Advanced ML demand forecasting (ARIMA, Prophet)
- Real-time inventory updates via WebSocket
- Enterprise SSO (SAML/OIDC)
- Advanced VRP route optimization
- Mobile-responsive PWA
- External ERP integrations
- Notification system (email, Slack)
- Advanced analytics and custom reports
- API rate limiting and throttling

---

## Version 3.0 — Enterprise Scale (Future)

- Kubernetes deployment manifests
- Distributed caching (Redis)
- Event-driven architecture (Kafka/RabbitMQ)
- ML training pipeline
- Advanced monitoring (Prometheus/Grafana)
- Multi-region deployment
- Advanced security (WAF, audit logs)
