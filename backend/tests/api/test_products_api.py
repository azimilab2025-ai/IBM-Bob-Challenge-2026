"""
API tests for /api/v1/products endpoints.
Tests: list, create, get, update.
"""
import pytest


class TestListProducts:
    def test_list_requires_auth(self, client):
        response = client.get("/api/v1/products")
        assert response.status_code == 401

    def test_list_returns_paginated(self, client, admin_headers, test_product):
        response = client.get("/api/v1/products", headers=admin_headers)
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert "meta" in body
        assert len(body["data"]) >= 1


class TestCreateProduct:
    def test_create_product_success(self, client, admin_headers):
        payload = {
            "name": "Laptop Model X",
            "sku": "LAP-X-001",
            "category": "Electronics",
            "unit": "unit",
            "unit_cost": 500.0,
            "unit_price": 799.99,
            "lead_time_days": 14,
        }
        response = client.post("/api/v1/products", headers=admin_headers, json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        data = body["data"]
        assert data["sku"] == "LAP-X-001"
        assert data["name"] == "Laptop Model X"

    def test_create_duplicate_sku_raises_conflict(self, client, admin_headers, test_product):
        payload = {
            "name": "Duplicate SKU Product",
            "sku": "SKU-TEST-001",  # same SKU as test_product fixture
        }
        response = client.post("/api/v1/products", headers=admin_headers, json=payload)
        assert response.status_code == 409

    def test_create_missing_required_fields(self, client, admin_headers):
        response = client.post("/api/v1/products", headers=admin_headers, json={"name": "No SKU"})
        assert response.status_code == 422


class TestGetProduct:
    def test_get_existing_product(self, client, admin_headers, test_product):
        prod_id = str(test_product.id)
        response = client.get(f"/api/v1/products/{prod_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["data"]["id"] == prod_id

    def test_get_nonexistent_product(self, client, admin_headers):
        import uuid
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/products/{fake_id}", headers=admin_headers)
        assert response.status_code == 404


class TestUpdateProduct:
    def test_update_product_success(self, client, admin_headers, test_product):
        prod_id = str(test_product.id)
        response = client.put(
            f"/api/v1/products/{prod_id}",
            headers=admin_headers,
            json={"name": "Updated Product Name", "unit_price": 20.0},
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Updated Product Name"
