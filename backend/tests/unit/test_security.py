"""Unit tests for security utilities — no DB dependency."""
import time
import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.exceptions import AuthenticationError


class TestPasswordHashing:

    def test_hash_is_different_from_plaintext(self):
        h = hash_password("secret123")
        assert h != "secret123"

    def test_verify_correct_password(self):
        h = hash_password("mypassword")
        assert verify_password("mypassword", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("mypassword")
        assert verify_password("wrongpassword", h) is False

    def test_hashes_are_unique(self):
        h1 = hash_password("same")
        h2 = hash_password("same")
        assert h1 != h2  # bcrypt generates unique salts


class TestJWT:

    def test_access_token_decode(self):
        token = create_access_token("user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"

    def test_refresh_token_type(self):
        token = create_refresh_token("user-456")
        payload = decode_token(token)
        assert payload["type"] == "refresh"
        assert payload["sub"] == "user-456"

    def test_additional_claims_embedded(self):
        token = create_access_token("user-1", {"role": "org_admin", "org_id": "org-1"})
        payload = decode_token(token)
        assert payload["role"] == "org_admin"
        assert payload["org_id"] == "org-1"

    def test_tampered_token_raises(self):
        token = create_access_token("user-123")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(AuthenticationError):
            decode_token(tampered)

    def test_invalid_token_raises(self):
        with pytest.raises(AuthenticationError):
            decode_token("not.a.real.token")
