"""Organization request/response schemas."""
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    is_active: Optional[bool] = None


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    address: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}
