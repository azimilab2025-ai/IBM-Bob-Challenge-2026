# Verification & Reproducibility Pack

## AI-Powered Supply Chain Optimization Platform

This document provides a concise, reproducible verification path for the challenge submission. It records the commands, environment assumptions, public evidence, measured AI outputs, validation results, and final-release checks required to verify the repository without modifying the core implementation.

> **Verification boundary:** The project uses deterministic synthetic demo data for reproducible evaluation. The measured values documented here demonstrate current system behavior and are not presented as production KPIs, customer-performance claims, or evidence of production-scale deployment.

---

## 1. Submission Snapshot

| Item | Verified Value |
|---|---|
| Project | AI-Powered Supply Chain Optimization Platform |
| Repository | https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026 |
| Live API | https://ibm-supply-chain-api.onrender.com |
| Interactive API Docs | https://ibm-supply-chain-api.onrender.com/docs |
| Health Check | https://ibm-supply-chain-api.onrender.com/health |
| Project Video | https://youtu.be/ZjQFvznSG1Y |
| Verified Runtime | Python 3.11.15 |
| Backend | FastAPI |
| Database | PostgreSQL |
| Containerization | Docker and Docker Compose |
| Automated Tests | 69 passed, 1 warning in 9.00 seconds |
| AI Evaluation | Completed successfully through `scripts/evaluate_ai.py` |
| Initial Functional Completion | Completed during the first 8 working days |
| Submission Hardening Verification | 2026-07-16 |
| Verified Application Commit | `e39d3b1df0b9ee2d711f2f7eff98df7c888e5d139` |
| Final Release Tag | `v1.0.0-submission-final` |
| Final Freeze Date | 2026-07-16 — effective after tag and GitHub Release publication |

The verified application commit records the tested and deployed implementation. The final release commit is identified by the annotated tag `v1.0.0-submission-final`, avoiding a self-referential commit hash inside this document.

---

## 2. Development Timeline and Change Boundary

The project timeline is documented transparently in two distinct phases.

### Initial Implementation Phase

The core project implementation was completed during the first 8 working days.

This phase included:

- backend architecture;
- database models and migrations;
- authentication and role-based access control;
- organizations, users, warehouses, products, inventory, and orders;
- demand forecasting;
- inventory optimization;
- warehouse allocation;
- route optimization;
- dashboard and report endpoints;
- automated tests;
- Swagger/OpenAPI documentation;
- Render deployment;
- demo authentication;
- project documentation and initial submission assets.

The system was considered functionally complete at the end of this phase.

### Submission Hardening and Verification Phase

After the initial functional completion, the following low-risk submission improvements were added and verified through 2026-07-15:

- Judge Quick Access;
- Judging Criteria Evidence;
- reproducible measured-results evaluation;
- `scripts/evaluate_ai.py`;
- `docs/verification.md`;
- explicit synthetic-data limitations;
- end-to-end decision workflow documentation;
- Python 3.11.15 compatibility verification;
- final automated-test verification;
- VS Code import-resolution configuration through `pyrightconfig.json`;
- release, reproducibility, and freeze documentation.

These later changes improve evidence quality, reproducibility, transparency, and judge accessibility. They do not represent a rewrite of the core business logic or a replacement of the initial implementation.

The final repository freeze will occur only after the final commit, push, release tag, GitHub Release, and live-service checks are completed.

---

## 3. Verification Principles

The verification process must remain:

- reproducible;
- read-only unless a setup command explicitly creates local development data;
- independent of the live production database;
- based on repository-controlled code;
- transparent about synthetic demo data;
- free from undocumented manual changes;
- repeatable by a reviewer or engineer;
- explicit about which checks are completed and which remain pending.

The AI evaluation script:

- does not connect to the database;
- does not call the live API;
- does not modify project files;
- does not require new third-party dependencies;
- executes the current forecasting, inventory, allocation, and routing implementations;
- produces deterministic results from a repository-controlled scenario.

---

## 4. Required Environment

### Core Requirements

| Dependency | Expected Version |
|---|---|
| Python | 3.11 |
| Verified Python Runtime | 3.11.15 |
| PostgreSQL | 15 or later |
| Git | Current supported release |
| Docker | Optional for container verification |
| Docker Compose | Optional for container verification |

### Verified macOS Python Installation

The final compatibility verification was performed using:

```text
Python 3.11.15
```

The verified Homebrew interpreter path was:

```text
/opt/homebrew/bin/python3.11
```

Reviewers may use another Python 3.11 installation when the exact Homebrew path is unavailable.

### Verify Local Tools

Run from a terminal:

```bash
python3 --version
git --version
docker --version
docker-compose --version
```

The Python command used for final verification must report a Python 3.11 runtime.

When a specific interpreter is required on macOS:

```bash
/opt/homebrew/bin/python3.11 --version
```

Expected verified output:

```text
Python 3.11.15
```

---

## 5. Repository Setup

Clone the repository and enter the project root:

```bash
git clone https://github.com/azimilab2025-ai/IBM-Bob-Challenge-2026.git
cd IBM-Bob-Challenge-2026
```

Create the local environment file:

```bash
cp .env.example .env
```

Create and activate the backend virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
```

Run database migrations:

```bash
alembic upgrade head
```

Seed the deterministic demo data:

```bash
python ../scripts/seed_data.py
```

Start the local API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Local verification endpoints:

| Resource | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## 6. Isolated Python 3.11 Verification Environment

To avoid modifying or replacing the project's existing local `.venv`, the final Python 3.11 compatibility verification used a separate temporary environment.

From the backend directory:

```bash
/opt/homebrew/bin/python3.11 -m venv /tmp/ibm-bob-py311-venv
```

Activate it:

```bash
source /tmp/ibm-bob-py311-venv/bin/activate
```

Install the backend and development dependencies:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
```

Verify the runtime:

```bash
python --version
```

Verified output:

```text
Python 3.11.15
```

This temporary environment:

- is separate from `backend/.venv`;
- does not modify the existing project environment;
- does not change application source files;
- can be removed after verification;
- exists only to confirm Python 3.11 compatibility safely.

---

## 7. Automated Test Verification

From the repository root:

```bash
cd backend
source /tmp/ibm-bob-py311-venv/bin/activate
python --version
python -m pytest -q
```

Final verified result:

```text
Python 3.11.15
69 passed, 1 warning in 9.00s
```

The test suite covers the core application behavior, including:

- authentication;
- authorization;
- repositories;
- services;
- API behavior;
- domain workflows;
- inventory operations;
- order operations;
- warehouse operations;
- security behavior;
- AI decision modules.

### Verified Warning Boundary

The single warning observed during the final test run was a Python deprecation warning emitted through the installed authentication dependency stack, specifically the legacy `crypt` integration used by `passlib`.

The warning:

- did not fail any test;
- did not change the test result;
- did not prevent Python 3.11.15 execution;
- did not indicate a regression in the project implementation.

It should be reviewed during future dependency maintenance, but it does not invalidate the verified result of 69 passing tests.

### Optional Coverage Report

```bash
python -m pytest --cov=app --cov=ai --cov-report=term-missing
```

The coverage command is provided for engineering inspection. Do not publish a coverage percentage unless it is generated and verified from the exact final commit.

---

## 8. Reproducible AI Evaluation

Return to the repository root while the Python 3.11 environment remains active:

```bash
cd ..
python scripts/evaluate_ai.py
```

A successful run must end with:

```text
Evaluation completed successfully.
```

Final verification status:

```text
Evaluation completed successfully.
```

### Verified Execution Boundary

The final evaluation was executed using:

| Verification Item | Result |
|---|---|
| Runtime | Python 3.11.15 |
| Execution Mode | Local |
| Database Access | None |
| Network Access | None |
| File Modification | None |
| Third-Party Dependency Addition | None |
| Result Type | Deterministic synthetic evaluation |

### Verified Measured Results

The following values were produced by the current deterministic synthetic evaluation scenario:

| Decision Area | Verified Result |
|---|---|
| Demand Forecasting | 7-day forecast: **142.00 units** |
| Forecast Daily Average | **20.2857 units/day** |
| Forecast One-Step Sample MAE | **4.00 units** |
| Inventory Safety Stock | **23.91 units** |
| Inventory Reorder Point | **83.91 units** |
| Recommended Order Quantity | **96.66 units** |
| Expected Shortage Risk | **5.0%** |
| Selected Warehouse | **Berlin West Fulfillment Center** |
| Selected Warehouse Score | **0.9756** |
| Second-Best Warehouse Score | **0.9102** |
| Warehouse Score Gap | **0.0654** |
| Initial Route Distance | **167.59 km** |
| Optimized Route Distance | **133.77 km** |
| Distance Saved | **33.82 km** |
| Measured Route Improvement | **20.18%** |

### Additional Verified Results

| Module | Additional Result |
|---|---|
| Forecasting | One-step holdout prediction: **21.00 units** versus actual demand of **25.00 units** |
| Inventory | Estimated holding cost: **$724.98** |
| Allocation | Berlin West **0.9756**, Leipzig Regional Hub **0.9102**, Potsdam Distribution Depot **0.6354** |
| Routing | `ORDER-FALKENSEE → ORDER-POTSDAM → ORDER-ERKNER → ORDER-ORANIENBURG` |
| Routing Duration | Estimated duration: **200 minutes** |

### Measurement Limitations

- The dataset is deterministic and synthetic.
- The forecasting MAE is a one-step sample holdout.
- The forecasting result is not a multi-period production benchmark.
- The route evaluation uses the current open-route implementation.
- The route evaluation excludes a return leg to the warehouse.
- Warehouse allocation uses the current configured scoring weights:
  - coverage: 70%;
  - proximity: 20%;
  - capacity: 10%.
- The measurements verify current baseline behavior rather than production-scale performance.
- No customer, revenue, production, or real-world KPI claim is made from these values.

---

## 9. Live Service Verification

### Public Health Check

Run:

```bash
curl -i https://ibm-supply-chain-api.onrender.com/health
```

Acceptance criteria:

- the service responds successfully;
- the response uses an HTTP success status;
- the endpoint confirms service availability;
- no secret or private configuration value appears in the response.

> The Render free instance may require 30–60 seconds to wake after inactivity.

### Swagger Verification

Open:

```text
https://ibm-supply-chain-api.onrender.com/docs
```

Verify that the following endpoint groups are visible:

- Authentication
- Users
- Organizations
- Warehouses
- Products
- Inventory
- Orders
- AI Insights
- Dashboard
- Reports
- Health

### Demo Authentication

Use the documented demo account only in the challenge demo environment:

```text
Email: admin@supplychain-demo.com
Password: SupplyChainDemo2026!
```

Authenticate through:

```text
POST /api/v1/auth/login
```

Then use the returned JWT access token through the Swagger **Authorize** control.

---

## 10. Recommended End-to-End Verification Path

Run the following workflow:

```text
Login
→ Dashboard Summary
→ Low-Stock Risk
→ Demand Forecast
→ Inventory Recommendation
→ Warehouse Allocation
→ Route Optimization
→ Measured Result
```

Recommended endpoints:

```text
POST /api/v1/auth/login
GET  /api/v1/dashboard/summary
GET  /api/v1/inventory/alerts/low-stock
POST /api/v1/ai/forecast/{product_id}
POST /api/v1/ai/optimize-inventory
POST /api/v1/orders/{id}/allocate
POST /api/v1/ai/optimize-routes
```

Acceptance criteria:

- authentication succeeds with the demo account;
- authorized endpoints accept the JWT token;
- each decision-support module returns a structured response;
- explanations are included where implemented;
- no cross-organization or unauthorized data is exposed;
- the health endpoint remains available.

---

## 11. Docker Compose Verification

From the repository root:

```bash
docker-compose up -d
```

Run migrations:

```bash
docker-compose exec backend alembic upgrade head
```

Seed demo data:

```bash
docker-compose exec backend python ../scripts/seed_data.py
```

Verify the health endpoint:

```bash
curl http://localhost:8000/health
```

Stop the local environment:

```bash
docker-compose down
```

Acceptance criteria:

- containers start without unrecoverable errors;
- migrations complete;
- demo data is created;
- the health endpoint responds successfully;
- containers stop cleanly.

Docker verification is optional when Docker is unavailable locally. It must not be marked complete unless the commands are actually executed successfully.

---

## 12. Repository Integrity Checks

Run from the repository root:

```bash
git status --short
```

Before the final commit, review every modified or untracked file.

Expected challenge-upgrade files include:

```text
README.md
docs/verification.md
scripts/evaluate_ai.py
pyrightconfig.json
```

No secrets or local-only artifacts should be committed.

Check ignored files:

```bash
git status --ignored --short
```

Confirm that the following remain uncommitted:

```text
.env
backend/.env
backend/.venv/
__pycache__/
.pytest_cache/
coverage artifacts
local database files
editor temporary files
operating-system metadata
```

The temporary verification environment is outside the repository and must not be committed:

```text
/tmp/ibm-bob-py311-venv/
```

Search for accidental credentials before release:

```bash
git grep -n -I -E "(SECRET_KEY|DATABASE_URL|API_KEY|PASSWORD|TOKEN)" -- .
```

Review every match and confirm that no real private secret is exposed.

Documented challenge demo credentials may appear only where they are intentionally provided for public evaluation.

---

## 13. Final Commit Record

After all tests and repository checks pass, create the final verification commit.

Display the current branch and status:

```bash
git branch --show-current
git status --short
```

Create the final commit:

```bash
git add README.md docs/verification.md scripts/evaluate_ai.py pyrightconfig.json
git commit -m "Add final judge evidence and reproducibility verification"
```

Push the verified commit:

```bash
git push origin main
```

The tested and deployed application commit is recorded as:

```text
e39d3b1df0b9ee2d711f2f7eff98df7c888e5d139
```

The final documentation commit must not attempt to contain its own hash. The annotated tag `v1.0.0-submission-final` identifies the immutable final release commit after this document is pushed.

---

## 14. Final Release Tag

Create the final annotated tag only after the final commit is pushed and verified:

```bash
git tag -a v1.0.0-submission-final -m "Final IBM Bob Challenge 2026 submission"
git push origin v1.0.0-submission-final
```

Recommended GitHub Release title:

```text
v1.0.0-submission-final
```

Recommended release description:

```text
Final verified version submitted to IBM SkillsBuild AI Builders with IBM Bob 2026.

Verification evidence:
- Live Render deployment
- Interactive Swagger documentation
- Demo authentication
- Python 3.11.15 compatibility verification
- 69 passing automated tests
- Reproducible AI evaluation script
- Measured forecasting, inventory, allocation, and routing outputs
- Judge Quick Access and Judging Criteria Evidence
- Verification and reproducibility documentation

The core implementation was completed during the initial eight-working-day development phase. Final evidence, documentation, compatibility validation, and release hardening continued through the final verification phase.

This tag identifies the frozen challenge-submission version.
```

---

## 15. Final Freeze Checklist

The repository is ready to freeze only when every required item below is confirmed.

### Public Evidence

- [x] Project video opens publicly.
- [x] GitHub repository opens publicly.
- [x] Swagger documentation opens publicly.
- [x] Health endpoint responds successfully.
- [x] Demo credentials authenticate successfully.

### Engineering Verification

- [x] Python 3.11.15 is installed and verified.
- [x] An isolated Python 3.11 verification environment was created.
- [x] Project and development dependencies installed successfully.
- [x] `python -m pytest -q` completed successfully.
- [x] The verified result is 69 passed, 1 warning in 9.00 seconds.
- [x] `python scripts/evaluate_ai.py` completed successfully.
- [x] Measured results match the documented deterministic scenario.
- [x] VS Code reports no unresolved import warnings caused by repository configuration.
- [ ] Docker Compose verification completes, when Docker is available.
- [x] `git status --short` is clean before the release-record update.
- [x] Secret and credential review is completed.

### Documentation Verification

- [x] Judge Quick Access is visible near the top of README.
- [x] Judging Criteria Evidence is documented.
- [x] Measured Results Snapshot matches the evaluation output.
- [x] Synthetic-data limitations are clearly stated.
- [x] The end-to-end decision workflow is documented.
- [x] `docs/verification.md` is linked from README.
- [x] Python 3.11.15 test evidence is recorded in this document.
- [x] The initial implementation phase and later verification phase are distinguished transparently.
- [x] The verified application commit is recorded in this document.
- [x] Final freeze date is recorded in this document.

### Release Verification

- [ ] Release-record commit is pushed to `main`.
- [x] Verified application commit is recorded.
- [ ] Tag `v1.0.0-submission-final` is pushed.
- [ ] GitHub Release is created.
- [ ] Release description identifies the frozen challenge version.
- [x] Render deployment is confirmed for the verified application commit.
- [x] Live health, Swagger, login, and authenticated profile checks are confirmed.
- [ ] No further code changes are made after the freeze without a new version.

---

## 16. Final Release Record

This record captures the verified application state. The final annotated tag and GitHub Release complete the repository freeze after this file is pushed.

| Record | Final Value |
|---|---|
| Final Branch | `main` |
| Verified Python Runtime | Python 3.11.15 |
| Final Test Result | 69 passed, 1 warning in 9.00 seconds |
| AI Evaluation | Completed successfully |
| AI Evaluation Script | `scripts/evaluate_ai.py` |
| Verified Application Commit | `e39d3b1df0b9ee2d711f2f7eff98df7c888e5d139` |
| Final Tag | `v1.0.0-submission-final` |
| Initial Functional Completion | First 8 working days |
| Submission Hardening Verification | 2026-07-16 |
| Final Freeze Date | 2026-07-16 — effective after tag and release publication |
| Live Health Check | Confirmed healthy on 2026-07-16 |
| Swagger Check | Confirmed publicly available on 2026-07-16 |
| Demo Authentication Check | Login and `/api/v1/auth/me` confirmed with HTTP 200 on 2026-07-16 |
| Project Video Check | Confirmed public |
| Repository Status | Clean before release-record update |
| GitHub Release | Create from `v1.0.0-submission-final` after the release commit is pushed |
| Render Deployment | Live on verified application commit `e39d3b1` on 2026-07-16 |

---

## 17. Evidence Statement

This repository provides a live, documented, tested, and reproducible demonstration of an AI-assisted supply-chain decision-support platform.

The verification evidence includes:

- public deployment;
- interactive API documentation;
- documented demo access;
- Python 3.11.15 compatibility verification;
- 69 passing automated tests;
- deterministic AI evaluation;
- measured decision outputs;
- architecture and implementation documentation;
- IBM Bob development-workflow evidence;
- a controlled final-release and freeze process;
- transparent separation between initial implementation and later submission-hardening work.

The project should be described as a production-oriented, multi-tenant, explainable decision-support platform.

Claims of production scale, autonomous decision-making, real-time optimization, guaranteed business impact, customer adoption, or commercial performance must not be made without additional operational evidence.
