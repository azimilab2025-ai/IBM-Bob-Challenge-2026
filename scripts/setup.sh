#!/usr/bin/env bash
# setup.sh — Local development setup script
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"

echo "=== Supply Chain Platform — Local Setup ==="

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is required but not found."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python $PYTHON_VERSION found."

# Environment file
if [ ! -f "$REPO_ROOT/.env" ]; then
    cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
    echo "Created .env from .env.example — update DATABASE_URL and SECRET_KEY before continuing."
    exit 0
fi

# Virtual environment
cd "$BACKEND_DIR"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
fi

source .venv/bin/activate

# Dependencies
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
pip install --quiet -r requirements-dev.txt
echo "Dependencies installed."

# Database migrations
echo "Running database migrations..."
alembic upgrade head

# Seed data
echo "Seeding initial data..."
cd "$REPO_ROOT"
python scripts/seed_data.py

echo ""
echo "=== Setup complete ==="
echo "Start the server with:"
echo "  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "API docs: http://localhost:8000/docs"
