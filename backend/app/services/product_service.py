"""Product service."""
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self, db: Session) -> None:
        self._repo = ProductRepository(Product, db)
        self._db = db

    def create(self, organization_id: uuid.UUID, data: ProductCreate) -> Product:
        if self._repo.sku_exists_in_org(data.sku, organization_id):
            raise ConflictError(
                f"Product with SKU '{data.sku}' already exists in this organization"
            )
        product = Product(organization_id=organization_id, **data.model_dump())
        return self._repo.create(product)

    def get_by_id(self, product_id: uuid.UUID, organization_id: uuid.UUID) -> Product:
        product = self._repo.get_by_id_and_org(product_id, organization_id)
        if not product:
            raise NotFoundError("Product", product_id)
        return product

    def list_by_org(
        self, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return self._repo.get_by_org(organization_id, skip=skip, limit=limit)

    def update(
        self, product_id: uuid.UUID, organization_id: uuid.UUID, data: ProductUpdate
    ) -> Product:
        product = self.get_by_id(product_id, organization_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        self._db.flush()
        self._db.refresh(product)
        return product
