"""Warehouse request/response schemas."""
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class WarehouseCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    code: str = Field(min_length=2, max_length=50)
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = Field(default=None, ge=0)


class WarehouseUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class WarehouseResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    code: str
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    capacity: Optional[int]
    is_active: bool

    model_config = {"from_attributes": True}
