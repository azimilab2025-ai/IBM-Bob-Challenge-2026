"""
API tests for system health endpoint.
"""
import pytest


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body.get("status") in ("ok", "healthy", "running")

    def test_root_redirects_or_returns(self, client):
        # Should at minimum not crash (200 or redirect)
        response = client.get("/", follow_redirects=False)
        assert response.status_code in (200, 301, 302, 307, 404)
