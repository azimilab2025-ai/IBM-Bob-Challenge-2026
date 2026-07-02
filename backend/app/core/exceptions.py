"""
Domain exception hierarchy.
All application errors should raise one of these exceptions.
Routers convert these to standardized HTTP responses.
"""
from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        error_code: str = "APP_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    """Resource does not exist."""

    def __init__(self, resource: str, identifier: Any) -> None:
        super().__init__(
            message=f"{resource} with id '{identifier}' not found",
            error_code="RESOURCE_NOT_FOUND",
            details={"resource": resource, "id": str(identifier)},
        )


class ConflictError(AppException):
    """Resource already exists or state conflict."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, error_code="CONFLICT", details=details)


class ValidationError(AppException):
    """Business rule validation failed."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message=message, error_code="VALIDATION_ERROR", details=details)


class AuthenticationError(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message=message, error_code="AUTHENTICATION_FAILED")


class AuthorizationError(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message=message, error_code="FORBIDDEN")


class InsufficientInventoryError(AppException):
    """Not enough stock to fulfill a request."""

    def __init__(self, product_id: str, requested: float, available: float) -> None:
        super().__init__(
            message=f"Insufficient inventory for product '{product_id}': requested {requested}, available {available}",
            error_code="INSUFFICIENT_INVENTORY",
            details={"product_id": product_id, "requested": requested, "available": available},
        )
