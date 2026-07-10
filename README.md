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

Use the following demo account in Swagger UI or through the `/api/v1/auth/login` endpoint:

```text
Email: admin@supplychain-demo.com
Password: SupplyChainDemo2026!
```

---

## 30-Second Judge Walkthrough

1. Open the live Swagger UI:  
   https://ibm-supply-chain-api.onrender.com/docs

2. Confirm the system is online using:

```text
GET /health
```

3. Log in using:

```text
POST /api/v1/auth/login
```

4. Click **Authorize** in Swagger and paste the returned access token.

5. Test the core platform endpoints:

```text
GET  /api/v1/dashboard/summary
GET  /api/v1/warehouses
GET  /api/v1/products
GET  /api/v1/inventory
POST /api/v1/ai/optimize-inventory
POST /api/v1/ai/optimize-routes
```

This demonstrates the deployed API, authentication, database connection, supply-chain data model, and AI-powered decision-support layer.

---

## Project Overview

The **AI-Powered Supply Chain Optimization Platform** is a full-stack supply-chain management system designed to help organizations make better operational decisions across warehouses, inventory, orders, and logistics.

The platform combines:

- A production-style FastAPI backend
- PostgreSQL database persistence
- JWT authentication and role-based access control
- Clean Architecture with routers, services, repositories, and models
- AI-assisted forecasting and optimization modules
- Interactive API documentation
- A frontend dashboard prototype
- Docker and cloud deployment readiness

The goal is to give supply-chain teams a practical decision-support system, not just a data viewer.

---

## What Problem Does This Solve?

Supply-chain teams often struggle with fragmented operational data and slow manual decision-making. Common problems include:

- No unified visibility across warehouses
- Stockouts caused by poor demand planning
- Overstock caused by inefficient replenishment
- Manual warehouse allocation for incoming orders
- Limited insight into reorder points and safety stock
- Slow reporting across products, orders, inventory, and warehouse activity
- No explainable AI layer to support operational decisions

This platform addresses those issues by turning supply-chain data into actionable recommendations.

---

## What the Platform Does

| Capability | Description |
|---|---|
| Inventory Management | Tracks stock levels across warehouses and products |
| Warehouse Management | Manages warehouse records, capacity, and operational data |
| Order Management | Supports order creation, allocation, and lifecycle tracking |
| AI Warehouse Allocation | Recommends the best warehouse for order fulfillment |
| Demand Forecasting | Provides demand forecasting using an extensible forecasting interface |
| Inventory Optimization | Calculates reorder points, safety stock, and replenishment recommendations |
| Route Optimization | Provides route-planning support with an extensible optimization interface |
| Dashboard KPIs | Shows management-level operational indicators |
| Reports | Provides inventory and operational reporting endpoints |
| Authentication | Uses JWT-based login, refresh, and current-user endpoints |
| Role-Based Access | Supports system admin, organization admin, warehouse, inventory, and operations roles |

Every AI recommendation is designed to be explainable and replaceable with more advanced models later.

---

## Demo & API Walkthrough

The platform includes a fully documented FastAPI backend with Swagger UI available at `/docs`.

The API covers:

- Authentication
- Users
- Organizations
- Warehouses
- Products
- Inventory
- Orders
- AI insights
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
│          HTML5 / CSS3 / Vanilla JS dashboard prototype       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ REST API /api/v1/
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     FastAPI Backend                          │
│                                                              │
│  Routers ──► Services ──► Repositories ──► ORM Models        │
│                 │                                            │
│                 └──► AI Modules                              │
│                      Forecasting / Inventory / Routing       │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
     ┌────────▼────────┐     ┌──────────▼──────────┐
     │   PostgreSQL    │     │  Alembic Migrations  │
     │  Primary DB     │     │  Schema Versioning   │
     └─────────────────┘     └─────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Routers | HTTP routes, request validation, response serialization |
| Services | Business logic, domain rules, transaction orchestration |
| Repositories | Database access and query logic |
| Models | SQLAlchemy ORM database models |
| Schemas | Pydantic request and response validation |
| AI Modules | Forecasting, optimization, allocation, and routing logic |
| Migrations | Database schema versioning with Alembic |

This separation keeps the project maintainable, testable, and ready for future model upgrades.

---

## AI Decision Layer

The AI layer is built as a modular decision-support system. Each module follows a defined interface so that baseline algorithms can later be replaced with more advanced models without rewriting the API or business logic.

| Module | Current Implementation | Future Extension |
|---|---|---|
| Warehouse Allocation | Score-based allocation using stock, capacity, and proximity | ML-based fulfillment recommendation |
| Demand Forecasting | Moving-average forecasting baseline | ARIMA, Prophet, LSTM, or transformer forecasting |
| Inventory Optimization | EOQ, safety stock, reorder points, and cost estimation | Stochastic optimization and multi-echelon inventory models |
| Route Optimization | Nearest-neighbor routing baseline | Vehicle Routing Problem solvers or geospatial optimization |

The current implementation is intentionally practical: it provides working recommendations now while preserving a clean path toward advanced AI models.

---

## Example Decision Outputs

| Decision Area | Platform Output |
|---|---|
| Demand Forecasting | Expected future demand for a selected product |
| Inventory Optimization | Recommended reorder quantity, safety stock, and reorder point |
| Warehouse Allocation | Suggested warehouse for fulfilling an order |
| Route Optimization | Suggested route sequence and estimated route distance |
| Dashboard | Low-stock alerts, order activity, inventory status, and KPIs |

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
| Authentication | JWT, python-jose, passlib, bcrypt |
| Validation | Pydantic |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Testing | pytest, httpx, SQLite in-memory |
| Deployment | Render |
| Containerization | Docker, Docker Compose |
| AI Assistance | IBM Bob |

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
# Edit .env and set DATABASE_URL, SECRET_KEY, and demo admin credentials

# 3. Create virtual environment and install dependencies
cd backend
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# 4. Run database migrations
alembic upgrade head

# 5. Seed demo data
python ../scripts/seed_data.py

# 6. Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Local access:

```text
API:         http://localhost:8000
Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
Health:      http://localhost:8000/health
```

---

### Docker Setup

```bash
# Start backend and database
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed demo data
python scripts/seed_data.py

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

# Unit tests
pytest tests/unit/ -v

# API tests
pytest tests/api/ -v

# Coverage report
pytest --cov=app --cov=ai --cov-report=term-missing
```

Test infrastructure uses SQLite in memory, so tests do not require a running PostgreSQL instance.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | System health check |
| POST | `/api/v1/auth/login` | Authenticate user and receive JWT tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current authenticated user |
| GET | `/api/v1/users` | List users |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/users/{user_id}` | Get user |
| PUT | `/api/v1/users/{user_id}` | Update user |
| GET | `/api/v1/organizations` | List organizations |
| POST | `/api/v1/organizations` | Create organization |
| GET | `/api/v1/warehouses` | List warehouses |
| POST | `/api/v1/warehouses` | Create warehouse |
| GET | `/api/v1/products` | List products |
| POST | `/api/v1/products` | Create product |
| GET | `/api/v1/inventory` | List inventory records |
| POST | `/api/v1/inventory` | Create or set inventory record |
| POST | `/api/v1/inventory/{id}/adjust` | Adjust stock quantity |
| GET | `/api/v1/inventory/alerts/low-stock` | Low-stock alerts |
| GET | `/api/v1/orders` | List orders |
| POST | `/api/v1/orders` | Create order |
| POST | `/api/v1/orders/{id}/allocate` | AI warehouse allocation |
| POST | `/api/v1/ai/forecast/{product_id}` | Demand forecasting |
| POST | `/api/v1/ai/optimize-inventory` | Inventory optimization |
| POST | `/api/v1/ai/optimize-routes` | Route optimization |
| GET | `/api/v1/dashboard/summary` | Management dashboard summary |
| GET | `/api/v1/reports/inventory` | Inventory report |

Full documentation is available in the deployed Swagger UI:

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
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── main.py
│   ├── ai/
│   ├── migrations/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
├── docs/
├── scripts/
├── assets/
│   ├── demo/
│   └── screenshots/
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
| [Architecture](docs/architecture.md) | System design, layers, and data model |
| [API Reference](docs/api.md) | Endpoint contracts and examples |
| [AI Modules](docs/ai-modules.md) | Forecasting and optimization logic |
| [Development Guide](docs/development-guide.md) | Local development workflow |
| [Deployment Guide](docs/deployment-guide.md) | Docker and cloud deployment notes |
| [Environment Variables](docs/environment-variables.md) | Required configuration values |
| [Testing Guide](docs/testing-guide.md) | Test strategy and commands |
| [Roadmap](docs/roadmap.md) | v1 status and future milestones |

---

## v1.0 Status

- [x] Public GitHub repository
- [x] Live Render deployment
- [x] FastAPI backend
- [x] PostgreSQL database connection
- [x] JWT authentication
- [x] Role-based access control
- [x] Organization management
- [x] Warehouse management
- [x] Product management
- [x] Inventory management
- [x] Order management
- [x] AI demand forecasting module
- [x] AI inventory optimization module
- [x] AI route optimization module
- [x] Dashboard summary endpoint
- [x] Reporting endpoints
- [x] Frontend dashboard prototype
- [x] Swagger API documentation
- [x] Docker and Docker Compose support
- [x] Alembic database migrations
- [x] Demo seed data
- [x] Test suite with 69 passing tests
- [x] IBM Bob-assisted development and troubleshooting
- [x] Challenge-ready documentation

---

## Roadmap

Future improvements may include:

- Dedicated production frontend deployment
- Advanced demand forecasting models
- Geospatial route optimization
- Real-time inventory events
- Supplier-risk scoring
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