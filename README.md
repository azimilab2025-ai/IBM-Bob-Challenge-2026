<p align="center">
  <h1 align="center">AI-Powered Supply Chain Optimization Platform</h1>
  <p align="center">
    Enterprise-grade platform for demand forecasting, inventory optimization, warehouse operations, and supply-chain decision support.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.11-green" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.104+-orange" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-blue" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/deployment-Render-brightgreen" alt="Deployment" />
  <img src="https://img.shields.io/badge/tests-69%20passed-brightgreen" alt="Tests" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License" />
</p>

<p align="center">
  <img
    src="assets/demo/supply-chain-optimization-platform-demo.gif"
    alt="AI-Powered Supply Chain Optimization Platform Demo"
    width="900"
  />
</p>

---

## Live Demo

The backend API is deployed on Render and can be tested directly through the interactive Swagger documentation.

| Resource | Link |
|---|---|
| Live API | https://ibm-supply-chain-api.onrender.com |
| Interactive API Docs | https://ibm-supply-chain-api.onrender.com/docs |
| Health Check | https://ibm-supply-chain-api.onrender.com/health |
| GitHub Repository | https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026 |

> Note: The live service uses Render's free instance type. If inactive, the first request may take 30–60 seconds while the service wakes up.

### Demo Login

Use the following demo account in Swagger UI through the `/api/v1/auth/login` endpoint:

```text
Email: admin@supplychain-demo.com
Password: SupplyChainDemo2026!
```

The root URL may return `{"detail":"Not Found"}` by design because the API is served through documented endpoints. Use `/docs` for testing and `/health` for status verification.

---

## 30-Second Judge Walkthrough

1. Open the live Swagger UI:

```text
https://ibm-supply-chain-api.onrender.com/docs
```

2. Run the health check:

```text
GET /health
```

3. Log in with the demo account:

```text
POST /api/v1/auth/login
```

4. Copy the returned JWT access token and click **Authorize** in Swagger.

5. Test the main decision-support endpoints:

```text
GET  /api/v1/dashboard/summary
GET  /api/v1/inventory/alerts/low-stock
POST /api/v1/orders/{id}/allocate
POST /api/v1/ai/forecast/{product_id}
POST /api/v1/ai/optimize-inventory
POST /api/v1/ai/optimize-routes
```

---

## Project Overview

The AI-Powered Supply Chain Optimization Platform is a full-stack decision-support system for supply-chain teams managing warehouses, products, inventory, orders, and operational reports.

The platform combines:

- Real-time inventory visibility
- Warehouse and order management
- Demand forecasting
- Inventory optimization
- Route optimization
- Role-based access control
- Dashboard KPIs and operational reports
- A deployed FastAPI backend with interactive Swagger documentation

The goal is to help teams move from fragmented operational data to faster, explainable, AI-assisted supply-chain decisions.

---

## What Problem Does This Solve?

Supply-chain teams often struggle with fragmented data, manual decision-making, and limited visibility across warehouses and inventory.

Common operational problems include:

- No unified inventory visibility across warehouses
- Stockouts caused by late replenishment decisions
- Overstock caused by poor demand forecasting
- Manual warehouse allocation for incoming orders
- Slow route planning and logistics decisions
- Limited KPI visibility for managers
- No clear decision-support layer between raw data and operations

This platform addresses these issues by turning operational data into structured recommendations that are explainable, testable, and available through a production API.

---

## What the Platform Does

| Capability | Description |
|---|---|
| Inventory Management | Tracks product stock levels across warehouses |
| Order Management | Supports order creation, tracking, allocation, and status updates |
| Warehouse Allocation | Recommends the best warehouse for fulfilling an order |
| Demand Forecasting | Estimates future product demand using historical demand patterns |
| Inventory Optimization | Calculates safety stock, reorder points, and recommended reorder quantities |
| Route Optimization | Suggests route sequence and estimated travel distance |
| Management Dashboard | Shows KPIs, inventory status, low-stock alerts, and recent order activity |
| Reports | Provides operational reports for inventory and management review |
| Authentication | JWT-based login and token refresh |
| Role-Based Access | Restricts access based on user responsibilities |

Every AI-assisted decision is designed to provide a recommendation plus a reason, not just a raw output.

---

## Technical Proof at a Glance

| Proof Area | Result |
|---|---|
| Backend framework | FastAPI |
| Runtime | Python 3.11 |
| Database | PostgreSQL on Render |
| Deployment | Live Render web service |
| API documentation | Swagger UI at `/docs` |
| Test suite | 69 passing tests |
| Architecture | Router → Service → Repository → Model |
| AI modules | 4 independent decision modules |
| Auth | JWT authentication |
| Access control | 5 user roles |
| Database schema | Multi-table relational schema with Alembic migrations |
| Frontend | Dashboard UI and API walkthrough assets |
| Documentation | Architecture, API, AI modules, testing, deployment, and environment guides |

---

## AI Decision Layer

The AI decision layer is separated from the core business logic. This makes the platform easier to test, explain, and upgrade.

| AI Module | Current Implementation | Output |
|---|---|---|
| Demand Forecasting | Moving-average baseline | Expected future demand |
| Inventory Optimization | EOQ-style reorder logic and safety stock calculation | Reorder quantity, safety stock, reorder point |
| Warehouse Allocation | Score-based warehouse selection | Recommended warehouse for an order |
| Route Optimization | Nearest-neighbor routing baseline | Suggested route sequence and estimated distance |

The current implementation focuses on explainable baseline algorithms that can later be replaced with advanced ML, optimization, or simulation models without rewriting the API or business layer.

---

## Example Decision Outputs

The following examples show the type of numerical decision support the platform provides. These values represent a demo supply-chain scenario and are intended to make the decision logic easy to evaluate.

| Decision Area | Example Input | Platform Output | Decision Impact |
|---|---|---|---|
| Demand Forecasting | Historical demand: 16, 18, 20, 21, 19, 23, 25 units/day | 7-day forecast: 142 units; average daily demand: 20.3 units | Helps plan purchasing before demand exceeds available stock |
| Inventory Optimization | Current stock: 38 units; average demand: 12/day; lead time: 5 days | Safety stock: 24 units; reorder point: 84 units; recommended reorder: 96 units | Flags a 46-unit gap before stockout risk becomes critical |
| Warehouse Allocation | Order quantity: 50 units; 3 candidate warehouses | Selected warehouse score: 0.91; next-best score: 0.74 | Chooses the strongest fulfillment location based on stock, capacity, and proximity |
| Route Optimization | 4 delivery points | Suggested route sequence: Warehouse → Stop 1 → Stop 3 → Stop 2 → Warehouse; estimated distance: 118.6 km | Converts delivery points into an optimized route sequence |
| Dashboard | Inventory, orders, warehouses, and AI alerts | Low-stock alerts, recent order activity, inventory status, and KPIs | Gives managers a single operational view |

### Impact Snapshot

| Metric | Before Platform | With Platform |
|---|---|---|
| Inventory visibility | Manual checks across separate records | Unified API and dashboard visibility |
| Reorder decisions | Reactive and delayed | Reorder point and safety-stock recommendation |
| Warehouse allocation | Manual comparison | Automated warehouse recommendation |
| Route planning | Manual route ordering | Suggested route sequence |
| Management reporting | Fragmented operational data | Dashboard KPIs and report endpoints |
| Technical confidence | Manual verification | 69 automated tests and documented API |

The platform is not only a dashboard. It is a decision-support backend that can expose operational recommendations through API endpoints, reports, and future enterprise integrations.

---

## Demo & API Walkthrough

The platform ships with a fully documented FastAPI backend. The interactive Swagger UI is available at `/docs`.

The API covers:

- Authentication
- Users
- Organizations
- Warehouses
- Products
- Inventory
- Orders
- AI recommendations
- Dashboard
- Reports
- Health checks

**API Documentation Screenshots**

| | |
|:---:|:---:|
| ![API Overview & Reports](assets/screenshots/01-api-overview-reports.jpg) | ![Authentication Flow](assets/screenshots/02-authentication-flow.jpg) |
| *API Overview & Reports* | *Authentication Flow* |
| ![Warehouses API](assets/screenshots/03-warehouses-api.jpg) | ![Inventory API](assets/screenshots/04-inventory-api.jpg) |
| *Warehouses API* | *Inventory API* |
| ![AI Insights API](assets/screenshots/05-ai-insights-api.jpg) | ![Dashboard & Reports](assets/screenshots/06-dashboard-reports-api.jpg) |
| *AI Insights API* | *Dashboard & Reports* |

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Dashboard                       │
│          HTML5 / CSS3 / Vanilla JavaScript                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ REST API /api/v1/
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     FastAPI Backend                          │
│                                                              │
│  Routers ──► Services ──► Repositories ──► ORM Models        │
│                 │                                            │
│                 └──► AI Decision Modules                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
     ┌────────▼────────┐     ┌──────────▼──────────┐
     │   PostgreSQL    │     │  Alembic Migrations  │
     │  Primary DB     │     │  Schema versioning    │
     └─────────────────┘     └─────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Routers | HTTP routing, request validation, and response serialization |
| Services | Business logic, domain rules, and transaction orchestration |
| Repositories | Database access and query isolation |
| Models | SQLAlchemy ORM definitions |
| Schemas | Pydantic request and response validation |
| AI Modules | Forecasting, optimization, allocation, and routing logic |
| Migrations | Version-controlled schema changes |

This structure keeps the system maintainable and prevents business logic from being mixed directly into API routes or database models.

---

## User Roles

| Role | Access |
|---|---|
| `system_admin` | Full platform access across all organizations |
| `org_admin` | Full access within one organization |
| `warehouse_manager` | Warehouse and inventory operations |
| `inventory_manager` | Inventory management and AI recommendations |
| `operations_manager` | Orders, dashboard, reports, and operational visibility |

Role-based access is enforced through the API and service layer.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Authentication | JWT, python-jose, passlib/bcrypt |
| Validation | Pydantic v2 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Testing | pytest, httpx, SQLite in-memory |
| Deployment | Render |
| Containerization | Docker, Docker Compose |
| Documentation | Markdown, Swagger/OpenAPI |

---

## IBM Bob Usage

This project was developed and improved with IBM Bob as the primary AI development assistant.

IBM Bob was used to support:

- Project structure and architecture planning
- Backend debugging and implementation support
- FastAPI endpoint design
- Authentication and role-based access refinement
- Database model and migration troubleshooting
- README and documentation improvement
- Render deployment troubleshooting
- Python version pinning for cloud deployment
- Environment-variable and production configuration review
- Final project-readiness improvements for the challenge submission

IBM Bob helped accelerate the development workflow while the final implementation, testing, debugging, deployment, and submission decisions were reviewed and completed by the project author.

---

## Quick Start

### Prerequisites

- Python 3.11
- PostgreSQL 15+
- Git
- Optional: Docker and Docker Compose

---

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026.git
cd IBM-Bob-Challenge-2026

# 2. Configure environment
cp .env.example .env

# 3. Create and activate a virtual environment
cd backend
python3 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
alembic upgrade head

# 6. Seed demo data
python ../scripts/seed_data.py

# 7. Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Local URLs:

| Resource | URL |
|---|---|
| API | `http://localhost:8000` |
| Swagger Docs | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| Health Check | `http://localhost:8000/health` |

---

### Docker Setup

```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed demo data
docker-compose exec backend python ../scripts/seed_data.py

# Verify health
curl http://localhost:8000/health
```

---

## Running Tests

```bash
cd backend
source .venv/bin/activate

# Run all tests
pytest -v

# Run unit tests
pytest tests/unit/ -v

# Run API tests
pytest tests/api/ -v

# Run coverage report
pytest --cov=app --cov=ai --cov-report=term-missing
```

Test summary:

| Test Area | Result |
|---|---|
| Unit tests | Passed |
| API tests | Passed |
| Total tests | 69 passed |
| Test database | SQLite in-memory |
| Production database | PostgreSQL |

The test suite validates the core business logic, API behavior, authentication flow, repositories, services, and AI decision modules.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/auth/login` | Authenticate and receive JWT tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |
| GET | `/api/v1/users` | List users |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/organizations` | List organizations |
| POST | `/api/v1/organizations` | Create organization |
| GET | `/api/v1/warehouses` | List warehouses |
| POST | `/api/v1/warehouses` | Create warehouse |
| GET | `/api/v1/products` | List products |
| POST | `/api/v1/products` | Create product |
| GET | `/api/v1/inventory` | List inventory |
| POST | `/api/v1/inventory` | Create or update inventory |
| POST | `/api/v1/inventory/{id}/adjust` | Adjust stock quantity |
| GET | `/api/v1/inventory/alerts/low-stock` | Low-stock alerts |
| GET | `/api/v1/orders` | List orders |
| POST | `/api/v1/orders` | Create order |
| POST | `/api/v1/orders/{id}/allocate` | AI warehouse allocation |
| POST | `/api/v1/ai/forecast/{product_id}` | Demand forecast |
| POST | `/api/v1/ai/optimize-inventory` | Inventory optimization |
| POST | `/api/v1/ai/optimize-routes` | Route optimization |
| GET | `/api/v1/dashboard/summary` | Management dashboard summary |
| GET | `/api/v1/reports/inventory` | Inventory report |

Full interactive API documentation is available at:

```text
https://ibm-supply-chain-api.onrender.com/docs
```

---

## Project Structure

```text
IBM-Bob-Challenge-2026/
├── backend/
│   ├── app/
│   │   ├── api/v1/routers/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── ai/
│   ├── migrations/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   ├── index.html
│   └── nginx.conf
├── assets/
│   ├── demo/
│   └── screenshots/
├── docs/
├── scripts/
├── docker-compose.yml
├── .env.example
├── .python-version
├── README.md
└── LICENSE
```

---

## Documentation

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | System design, data flow, and layer responsibilities |
| [API Reference](docs/api.md) | Endpoint contracts and examples |
| [AI Modules](docs/ai-modules.md) | Forecasting, optimization, allocation, and routing logic |
| [Development Guide](docs/development-guide.md) | Local setup and development workflow |
| [Deployment Guide](docs/deployment-guide.md) | Docker and cloud deployment notes |
| [Environment Variables](docs/environment-variables.md) | Required configuration values |
| [Testing Guide](docs/testing-guide.md) | Test structure and execution guide |
| [Roadmap](docs/roadmap.md) | Completed work and future improvements |

---

## v1.0 Status

- [x] Clean Architecture project structure
- [x] FastAPI backend
- [x] PostgreSQL database configuration
- [x] SQLAlchemy ORM models
- [x] Alembic migrations
- [x] JWT authentication
- [x] Role-based access control
- [x] Organization, user, warehouse, product, inventory, and order modules
- [x] Demand forecasting module
- [x] Inventory optimization module
- [x] Warehouse allocation module
- [x] Route optimization module
- [x] Dashboard and reporting endpoints
- [x] Swagger/OpenAPI documentation
- [x] Render live deployment
- [x] Demo login account
- [x] 69 passing tests
- [x] README with live demo, judge walkthrough, IBM Bob usage, and decision-output proof

---

## Roadmap

Future improvements could include:

- Dedicated production frontend deployment
- Advanced demand forecasting models
- Geospatial route optimization
- Real-time inventory events
- Supplier risk scoring
- Multi-tenant organization dashboards
- Extended analytics and exportable reports
- CI/CD pipeline with automated tests

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with IBM Bob · IBM SkillsBuild AI Builders with IBM Bob 2026
</p>