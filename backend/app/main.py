"""
Supply Chain Optimization Platform — FastAPI application entry point.
Initializes the app, registers middleware, registers routers, and sets up
exception handlers following the project's standard response contract.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    ValidationError as AppValidationError,
)
from app.core.logging import configure_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    settings = get_settings()
    configure_logging()
    logger.info(
        "Starting %s v%s in %s mode",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.APP_ENV,
    )
    yield
    logger.info("Application shutting down")


def create_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-Powered Enterprise Supply Chain Optimization Platform. "
            "Manage warehouses, inventory, orders, and leverage AI for "
            "demand forecasting, warehouse allocation, and inventory optimization."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # Exception handlers — convert domain exceptions to HTTP responses
    # ------------------------------------------------------------------

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": exc.error_code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"success": False, "error": exc.error_code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(AppValidationError)
    async def validation_handler(request: Request, exc: AppValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": exc.error_code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"success": False, "error": exc.error_code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_handler(request: Request, exc: AuthorizationError) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": exc.error_code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": exc.error_code, "message": exc.message, "details": exc.details},
        )

    # ------------------------------------------------------------------
    # Routers
    # ------------------------------------------------------------------
    from app.api.v1.routers import health
    from app.api.v1.routers import auth
    from app.api.v1.routers import users
    from app.api.v1.routers import organizations
    from app.api.v1.routers import warehouses
    from app.api.v1.routers import products
    from app.api.v1.routers import inventory
    from app.api.v1.routers import orders
    from app.api.v1.routers import ai as ai_router
    from app.api.v1.routers import dashboard
    from app.api.v1.routers import reports

    API_PREFIX = "/api/v1"

    app.include_router(health.router, tags=["System"])
    app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["Authentication"])
    app.include_router(users.router, prefix=f"{API_PREFIX}/users", tags=["Users"])
    app.include_router(organizations.router, prefix=f"{API_PREFIX}/organizations", tags=["Organizations"])
    app.include_router(warehouses.router, prefix=f"{API_PREFIX}/warehouses", tags=["Warehouses"])
    app.include_router(products.router, prefix=f"{API_PREFIX}/products", tags=["Products"])
    app.include_router(inventory.router, prefix=f"{API_PREFIX}/inventory", tags=["Inventory"])
    app.include_router(orders.router, prefix=f"{API_PREFIX}/orders", tags=["Orders"])
    app.include_router(ai_router.router, prefix=f"{API_PREFIX}/ai", tags=["AI Insights"])
    app.include_router(dashboard.router, prefix=f"{API_PREFIX}/dashboard", tags=["Dashboard"])
    app.include_router(reports.router, prefix=f"{API_PREFIX}/reports", tags=["Reports"])

    return app


app = create_application()
