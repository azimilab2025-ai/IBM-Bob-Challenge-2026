"""
Centralized authentication and security utilities.
All JWT operations and password hashing must go through this module.
No other module should implement auth logic.
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------------------
# Password utilities
# ---------------------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    """Hash a plaintext password. Returns a bcrypt hash."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return _pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT utilities
# ---------------------------------------------------------------------------

def create_access_token(
    subject: str,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: The user's unique identifier (UUID as string).
        additional_claims: Extra claims to embed (e.g., role, org_id).

    Returns:
        Signed JWT string.
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "type": "access",
    }
    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """
    Create a signed JWT refresh token with longer TTL.

    Args:
        subject: The user's unique identifier.

    Returns:
        Signed JWT string.
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.

    Raises:
        AuthenticationError: If token is invalid or expired.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise AuthenticationError(f"Invalid or expired token: {str(e)}")


def extract_user_id(token: str) -> str:
    """Extract the user ID (sub claim) from a token."""
    payload = decode_token(token)
    subject = payload.get("sub")
    if not subject:
        raise AuthenticationError("Token missing subject claim")
    return subject
