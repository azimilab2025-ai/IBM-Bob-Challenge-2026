"""Order service — order creation and lifecycle management."""
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService:

    def __init__(self, db: Session) -> None:
        self._repo = OrderRepository(Order, db)
        self._prod_repo = ProductRepository(Product, db)
        self._db = db

    def create(self, organization_id: uuid.UUID, created_by: uuid.UUID, data: OrderCreate) -> Order:
        if self._repo.reference_exists(data.reference_number):
            raise ConflictError(
                f"Order reference '{data.reference_number}' already exists"
            )

        # Validate all products belong to the organization
        for item_data in data.items:
            product = self._prod_repo.get_by_id_and_org(item_data.product_id, organization_id)
            if not product:
                raise ValidationError(
                    f"Product '{item_data.product_id}' not found in this organization"
                )

        order = Order(
            organization_id=organization_id,
            created_by=created_by,
            reference_number=data.reference_number,
            priority=data.priority,
            delivery_address=data.delivery_address,
            delivery_latitude=data.delivery_latitude,
            delivery_longitude=data.delivery_longitude,
            notes=data.notes,
            status=OrderStatus.PENDING,
        )
        self._db.add(order)
        self._db.flush()

        total = 0.0
        for item_data in data.items:
            item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                notes=item_data.notes,
            )
            self._db.add(item)
            if item_data.unit_price:
                total += item_data.quantity * item_data.unit_price

        order.total_amount = total if total > 0 else None
        self._db.flush()
        self._db.refresh(order)
        return order

    def get_by_id(self, order_id: uuid.UUID, organization_id: uuid.UUID) -> Order:
        order = self._repo.get_by_id_with_items(order_id)
        if not order or order.organization_id != organization_id:
            raise NotFoundError("Order", order_id)
        return order

    def list_by_org(
        self,
        organization_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[OrderStatus] = None,
    ) -> List[Order]:
        return self._repo.get_by_org(organization_id, skip=skip, limit=limit, status=status)

    def update_status(
        self, order_id: uuid.UUID, organization_id: uuid.UUID, data: OrderUpdate
    ) -> Order:
        order = self.get_by_id(order_id, organization_id)
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(order, field, value)
        self._db.flush()
        self._db.refresh(order)
        return order
