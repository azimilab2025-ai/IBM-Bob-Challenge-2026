"""Products router — product catalog management."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUserContext, get_current_user_context
from app.db.session import get_db
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ProductResponse], summary="List Products")
def list_products(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """List active products for the current organization."""
    org_id = ctx.resolve_org_id()
    svc = ProductService(db)
    skip = (page - 1) * per_page
    items = svc.list_by_org(org_id, skip=skip, limit=per_page)
    from app.repositories.product_repository import ProductRepository
    from app.models.product import Product
    total = ProductRepository(Product, db).count_by_org(org_id)
    return PaginatedResponse(
        data=[ProductResponse.model_validate(p) for p in items],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, total_pages=max(1, -(-total // per_page))),
    )


@router.post("", response_model=SuccessResponse[ProductResponse], status_code=201, summary="Create Product")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Create a new product in the current organization."""
    ctx.require_role("system_admin", "org_admin", "inventory_manager")
    org_id = ctx.resolve_org_id()
    svc = ProductService(db)
    product = svc.create(org_id, data)
    db.commit()
    db.refresh(product)
    return SuccessResponse(data=ProductResponse.model_validate(product), message="Product created")


@router.get("/{product_id}", response_model=SuccessResponse[ProductResponse], summary="Get Product")
def get_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Get a single product by ID."""
    org_id = ctx.resolve_org_id()
    svc = ProductService(db)
    product = svc.get_by_id(product_id, org_id)
    return SuccessResponse(data=ProductResponse.model_validate(product))


@router.put("/{product_id}", response_model=SuccessResponse[ProductResponse], summary="Update Product")
def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    ctx: CurrentUserContext = Depends(get_current_user_context),
):
    """Update product details."""
    ctx.require_role("system_admin", "org_admin", "inventory_manager")
    org_id = ctx.resolve_org_id()
    svc = ProductService(db)
    product = svc.update(product_id, org_id, data)
    db.commit()
    db.refresh(product)
    return SuccessResponse(data=ProductResponse.model_validate(product), message="Product updated")
