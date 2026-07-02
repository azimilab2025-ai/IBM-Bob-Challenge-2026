"""Product request/response schemas."""
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    unit: str = "unit"
    unit_cost: Optional[float] = Field(default=None, ge=0)
    unit_price: Optional[float] = Field(default=None, ge=0)
    reorder_point: Optional[float] = Field(default=None, ge=0)
    lead_time_days: Optional[int] = Field(default=None, ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    unit_cost: Optional[float] = Field(default=None, ge=0)
    unit_price: Optional[float] = Field(default=None, ge=0)
    reorder_point: Optional[float] = Field(default=None, ge=0)
    lead_time_days: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    sku: str
    description: Optional[str]
    category: Optional[str]
    unit: str
    unit_cost: Optional[float]
    unit_price: Optional[float]
    reorder_point: Optional[float]
    lead_time_days: Optional[int]
    is_active: bool

    model_config = {"from_attributes": True}
