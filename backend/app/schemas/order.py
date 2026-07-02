"""Order request/response schemas."""
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.order import OrderPriority, OrderStatus


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: float = Field(gt=0)
    unit_price: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    reference_number: str = Field(min_length=1, max_length=100)
    priority: OrderPriority = OrderPriority.NORMAL
    delivery_address: Optional[str] = None
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    notes: Optional[str] = None
    items: List[OrderItemCreate] = Field(min_length=1)


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    priority: Optional[OrderPriority] = None
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: float
    unit_price: Optional[float]
    notes: Optional[str]

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    reference_number: str
    status: OrderStatus
    priority: OrderPriority
    delivery_address: Optional[str]
    delivery_latitude: Optional[float]
    delivery_longitude: Optional[float]
    notes: Optional[str]
    total_amount: Optional[float]
    items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True}
