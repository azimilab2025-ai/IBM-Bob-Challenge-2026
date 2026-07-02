<p align="center">
  <h1 align="center">AI-Powered Supply Chain Optimization Platform</h1>
  <p align="center">Enterprise-grade platform for intelligent supply chain management, demand forecasting, and operational decision-making</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.11+-green" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.104+-orange" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-blue" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License" />
</p>

---

## Overview

This platform solves a core enterprise problem: organizations managing multiple warehouses, products, and orders lack reliable tools to make fast, intelligent operational decisions.

This system provides:
- **Full operational visibility** across inventory, warehouses, and orders
- **AI-powered decision support** for warehouse allocation, demand forecasting, and inventory optimization
- **Management dashboard** for real-time KPIs and operational alerts
- **RESTful API** designed for extensibility and SaaS readiness

---

## Problem Statement

Organizations face:
- No unified inventory visibility across warehouses
- Slow, manual warehouse-to-order allocation
- Unreliable demand forecasting
- Inventory shortages or overstock situations
- No decision-support layer between raw data and management

---

## Solution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Dashboard                       │
│           (HTML/CSS/JS — Component-based, SPA-ready)        │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (v1)
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  │
│  │  Routers │  │ Services │  │   Repos   │  │  Models  │  │
│  └──────────┘  └──────────┘  └───────────┘  └──────────┘  │
└──────────────────────────┬──────────────────────────────────┘
           ┌───────────────┼───────────────┐
           │               │               │
┌──────────▼──────┐ ┌──────▼──────┐ ┌─────▼───────────────┐
│   PostgreSQL    │ │  AI Modules │ │  Migrations (Alembic)│
│   (Primary DB)  │ │ (Pluggable) │ │                      │
└─────────────────┘ └─────────────┘ └──────────────────────┘
```

---

## Core Features (v1.0)

| Module | Description |
|--------|-------------|
| **Authentication** | JWT-based auth with role-aware access control |
| **Organizations** | Multi-organization support with isolated data |
| **Warehouses** | Warehouse management with capacity and location |
| **Products** | Product catalog per organization |
| **Inventory** | Real-time inventory tracking per product/warehouse |
| **Orders** | Order management with multi-item support |
| **Warehouse Allocation** | AI-powered optimal warehouse selection per order |
| **Demand Forecasting** | Moving average forecasting (pluggable architecture) |
| **Inventory Optimization** | EOQ, safety stock, reorder point recommendations |
| **Route Optimization** | Basic operational routing (extensible to VRP) |
| **Dashboard** | KPIs, alerts, recent activity, AI insights |
| **Reports** | Operational and management reports |

---

## User Roles

| Role | Capabilities |
|------|-------------|
| `system_admin` | Full system access, all organizations |
| `org_admin` | Manage users, warehouses, products, orders within org |
| `warehouse_manager` | Manage warehouse data and inventory |
| `inventory_manager` | Manage inventory levels, view recommendations |
| `operations_manager` | View orders, allocations, dashboard, reports |

---

## AI Modules

Each AI module is **independently pluggable** — swap algorithms without touching Business Logic:

- **Warehouse Allocation Engine**: Scores warehouses by inventory availability, capacity, and proximity
- **Demand Forecasting**: Moving average baseline; interface supports ML/DL models
- **Inventory Optimizer**: EOQ-based safety stock, reorder point, and cost estimation
- **Route Optimizer**: Basic operational routing; extensible to full VRP

All AI decisions are **explainable** — each recommendation includes the reasoning behind it.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL 15+, SQLAlchemy 2.x, Alembic |
| Authentication | JWT (python-jose), bcrypt |
| Validation | Pydantic v2 |
| Frontend | HTML5, CSS3, Vanilla JS (component-based) |
| Containerization | Docker, Docker Compose |
| Testing | pytest, httpx |

---

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026.git
cd IBM-Bob-Challenge-2026

# 2. Configure environment
cp .env.example .env
# Edit .env with your database credentials and secret key

# 3. Create virtual environment
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
alembic upgrade head

# 6. Seed initial data
python ../scripts/seed_data.py

# 7. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Setup

```bash
# Start all services (PostgreSQL + Backend + Frontend)
docker-compose up -d

# Run migrations inside container
docker-compose exec backend alembic upgrade head

# Access the application
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Frontend: http://localhost:8080
```

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Base URL: `/api/v1/`

---

## Project Structure

```
IBM-Bob-Challenge-2026/
├── backend/
│   ├── app/
│   │   ├── api/v1/routers/     # HTTP route handlers (no business logic)
│   │   ├── core/               # Config, security, dependencies, logging
│   │   ├── db/                 # Database session and base
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── repositories/       # Database access layer
│   │   ├── services/           # Business logic layer
│   │   └── main.py             # Application entry point
│   ├── ai/                     # Independent AI modules
│   │   ├── interfaces/         # Abstract base interfaces
│   │   ├── demand_forecasting/
│   │   ├── warehouse_allocation/
│   │   ├── inventory_optimization/
│   │   └── route_optimization/
│   ├── migrations/             # Alembic migration scripts
│   └── tests/                  # Unit, integration, API tests
├── frontend/
│   └── src/                    # HTML pages, JS modules, CSS
├── docs/                       # Architecture, API, guides
├── scripts/                    # Setup and seed scripts
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture Overview](docs/architecture.md) | System design and layer responsibilities |
| [API Documentation](docs/api.md) | Endpoint contracts and examples |
| [Development Guide](docs/development-guide.md) | Local setup and contribution workflow |
| [Deployment Guide](docs/deployment-guide.md) | Docker and cloud deployment |
| [Environment Variables](docs/environment-variables.md) | All configuration options |
| [AI Modules](docs/ai-modules.md) | AI architecture and algorithms |
| [Testing Guide](docs/testing-guide.md) | Test structure and how to run |
| [Roadmap](docs/roadmap.md) | v1 status and future milestones |

---

## Status

**Version 1.0 — Active Development**

- [x] Repository structure and architecture
- [ ] Configuration and database setup
- [ ] Core models and schemas
- [ ] Authentication system
- [ ] Organization and user management
- [ ] Warehouse and inventory management
- [ ] Order management
- [ ] AI modules
- [ ] Frontend dashboard
- [ ] Testing suite
- [ ] Deployment configuration

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">Built with IBM Bob · IBM TechXChange Challenge 2026</p>
