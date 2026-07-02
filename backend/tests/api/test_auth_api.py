"""
API tests for /api/v1/auth endpoints.
Tests: login, token refresh, /me profile endpoint.
"""
import pytest


class TestLogin:
    def test_login_success(self, client, test_admin):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "TestPass123!"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        data = body["data"]
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    def test_login_wrong_password(self, client, test_admin):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "WrongPass!"},
        )
        assert response.status_code == 401
        assert response.json()["success"] is False

    def test_login_unknown_email(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@nowhere.com", "password": "Whatever1!"},
        )
        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        response = client.post("/api/v1/auth/login", json={"email": "x@x.com"})
        assert response.status_code == 422


class TestRefreshToken:
    def test_refresh_success(self, client, test_admin):
        login_resp = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "TestPass123!"},
        )
        refresh_token = login_resp.json()["data"]["refresh_token"]

        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "access_token" in body["data"]

    def test_refresh_invalid_token(self, client):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"},
        )
        assert response.status_code == 401


class TestGetMe:
    def test_get_me_authenticated(self, client, admin_headers, test_admin):
        response = client.get("/api/v1/auth/me", headers=admin_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["email"] == "admin@test.com"
        assert body["data"]["role"] == "system_admin"

    def test_get_me_unauthenticated(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
