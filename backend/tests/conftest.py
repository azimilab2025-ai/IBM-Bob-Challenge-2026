"""
Pytest configuration and shared fixtures for all tests.
Uses SQLite in-memory database to avoid requiring a live PostgreSQL instance.
Overrides the FastAPI app's get_db dependency for full isolation.
"""
import os
import uuid
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

# ── Set env vars BEFORE importing app modules ──────────────────────────────
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY",   "test-secret-key-that-is-at-least-32-chars!!")
os.environ.setdefault("APP_ENV",      "development")
os.environ.setdefault("DEBUG",        "false")

# Clear lru_cache so Settings picks up the env vars above
from app.core.config import get_settings
get_settings.cache_clear()

from app.db.base import Base
from app.db.session import get_db
from app.main import create_application
from app.core.security import create_access_token, hash_password
from app.models.organization import Organization
from app.models.user import User, UserRole
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.inventory import InventoryItem
from app.models.order import Order, OrderItem, OrderStatus, OrderPriority

# ── SQLite test engine ──────────────────────────────────────────────────────

SQLITE_URL = "sqlite:///:memory:"

_test_engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
)

# SQLite does not enforce foreign key constraints by default
@event.listens_for(_test_engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=_test_engine,
)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once per test session."""
    Base.metadata.create_all(bind=_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    """Provide a transactional DB session that rolls back after each test."""
    connection = _test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    FastAPI TestClient with get_db overridden to use the test session.
    Each test gets a clean database state.
    """
    app = create_application()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
    app.dependency_overrides.clear()


# ── Shared data fixtures ────────────────────────────────────────────────────

@pytest.fixture()
def test_org(db: Session) -> Organization:
    """A persisted test organization."""
    org = Organization(name="Test Organization", is_active=True)
    db.add(org)
    db.flush()
    return org


@pytest.fixture()
def test_admin(db: Session, test_org: Organization) -> User:
    """A system admin user."""
    user = User(
        email="admin@test.com",
        full_name="Test Admin",
        hashed_password=hash_password("TestPass123!"),
        role=UserRole.SYSTEM_ADMIN,
        organization_id=test_org.id,
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def test_user(db: Session, test_org: Organization) -> User:
    """An org_admin user."""
    user = User(
        email="orgadmin@test.com",
        full_name="Org Admin",
        hashed_password=hash_password("TestPass123!"),
        role=UserRole.ORG_ADMIN,
        organization_id=test_org.id,
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def admin_token(test_admin: User) -> str:
    """JWT access token for the system admin."""
    return create_access_token(
        str(test_admin.id),
        {
            "role": test_admin.role.value,
            "org_id": str(test_admin.organization_id),
        },
    )


@pytest.fixture()
def user_token(test_user: User) -> str:
    """JWT access token for the org admin."""
    return create_access_token(
        str(test_user.id),
        {
            "role": test_user.role.value,
            "org_id": str(test_user.organization_id),
        },
    )


@pytest.fixture()
def admin_headers(admin_token: str) -> dict:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture()
def user_headers(user_token: str) -> dict:
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture()
def test_warehouse(db: Session, test_org: Organization) -> Warehouse:
    wh = Warehouse(
        organization_id=test_org.id,
        name="Test Warehouse",
        code="WH-TEST",
        city="New York",
        country="US",
        latitude=40.7128,
        longitude=-74.0060,
        capacity=10000,
        is_active=True,
    )
    db.add(wh)
    db.flush()
    return wh


@pytest.fixture()
def test_product(db: Session, test_org: Organization) -> Product:
    product = Product(
        organization_id=test_org.id,
        name="Test Product",
        sku="SKU-TEST-001",
        category="Electronics",
        unit="unit",
        unit_cost=10.0,
        unit_price=15.0,
        reorder_point=20.0,
        lead_time_days=7,
        is_active=True,
    )
    db.add(product)
    db.flush()
    return product


@pytest.fixture()
def test_inventory(db: Session, test_product: Product, test_warehouse: Warehouse) -> InventoryItem:
    item = InventoryItem(
        product_id=test_product.id,
        warehouse_id=test_warehouse.id,
        quantity_on_hand=100.0,
        quantity_reserved=0.0,
        reorder_point=20.0,
        safety_stock=10.0,
    )
    db.add(item)
    db.flush()
    return item


@pytest.fixture()
def test_order(db: Session, test_org: Organization, test_admin: User, test_product: Product) -> Order:
    import uuid as _uuid
    order = Order(
        organization_id=test_org.id,
        created_by=test_admin.id,
        reference_number=f"ORD-TEST-{str(_uuid.uuid4())[:8].upper()}",
        status=OrderStatus.PENDING,
        priority=OrderPriority.NORMAL,
        delivery_address="123 Test St",
        delivery_latitude=40.7128,
        delivery_longitude=-74.0060,
    )
    db.add(order)
    db.flush()

    item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=10.0,
        unit_price=15.0,
    )
    db.add(item)
    db.flush()
    return order
