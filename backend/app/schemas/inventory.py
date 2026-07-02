"""Inventory request/response schemas."""
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class InventoryCreate(BaseModel):
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    quantity_on_hand: float = Field(default=0.0, ge=0)
    reorder_point: Optional[float] = Field(default=None, ge=0)
    safety_stock: Optional[float] = Field(default=None, ge=0)


class InventoryUpdate(BaseModel):
    quantity_on_hand: Optional[float] = Field(default=None, ge=0)
    quantity_reserved: Optional[float] = Field(default=None, ge=0)
    reorder_point: Optional[float] = Field(default=None, ge=0)
    safety_stock: Optional[float] = Field(default=None, ge=0)


class InventoryAdjust(BaseModel):
    """Adjust inventory by a delta (positive = add, negative = remove)."""
    delta: float
    reason: Optional[str] = None


class InventoryResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    quantity_on_hand: float
    quantity_reserved: float
    quantity_available: float
    reorder_point: Optional[float]
    safety_stock: Optional[float]
    is_low_stock: bool

    model_config = {"from_attributes": True}
