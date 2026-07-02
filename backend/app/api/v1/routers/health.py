"""Health check endpoint — no authentication required."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import get_db

router = APIRouter()


@router.get("/health", summary="Health Check")
def health_check(db: Session = Depends(get_db)):
    """Returns application health status including database connectivity."""
    settings = get_settings()
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
