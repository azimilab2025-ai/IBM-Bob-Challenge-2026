"""
Centralized structured logging configuration.
All application logging must use the logger obtained from this module.
"""
import logging
import sys
from typing import Optional

from app.core.config import get_settings


def configure_logging(log_level: Optional[str] = None) -> None:
    """Configure root logger with structured format."""
    settings = get_settings()
    level = log_level or settings.LOG_LEVEL

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
        if not settings.is_production
        else '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","line":%(lineno)d,"message":"%(message)s"}'
    )

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=log_format,
        datefmt="%Y-%m-%dT%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )

    # Suppress noisy third-party loggers in production
    if settings.is_production:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger. Use module __name__ as the name."""
    return logging.getLogger(name)
