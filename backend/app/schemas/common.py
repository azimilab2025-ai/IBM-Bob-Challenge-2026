"""
Shared Pydantic schemas used across all modules.
All API responses must follow the standard envelope defined here.
"""
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class SuccessResponse(BaseModel, Generic[DataT]):
    """Standard success response envelope."""
    success: bool = True
    data: DataT
    message: str = "Operation completed successfully"


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Standard paginated list response envelope."""
    success: bool = True
    data: List[DataT]
    message: str = "Data retrieved successfully"
    meta: "PaginationMeta"


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class ErrorResponse(BaseModel):
    """Standard error response envelope."""
    success: bool = False
    error: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class PaginationParams(BaseModel):
    """Common pagination query parameters."""
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page
