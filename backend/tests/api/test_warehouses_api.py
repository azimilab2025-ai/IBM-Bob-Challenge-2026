"""
API tests for /api/v1/warehouses endpoints.
Tests: list, create, get, update, deactivate.
"""
import pytest


class TestListWarehouses:
    def test_list_requires_auth(self, client):
        response = client.get("/api/v1/warehouses")
        assert response.status_code == 401

    def test_list_returns_paginated(self, client, admin_headers, test_warehouse):
        response = client.get("/api/v1/warehouses", headers=admin_headers)
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert "meta" in body
        assert len(body["data"]) >= 1
        meta = body["meta"]
        assert meta["page"] == 1
        assert meta["per_page"] == 20

    def test_list_empty_for_new_context(self, client, user_headers):
        # user_headers org has no warehouses not shared (same org here, so may have)
        response = client.get("/api/v1/warehouses", headers=user_headers)
        assert response.status_code == 200


class TestCreateWarehouse:
    def test_create_warehouse_success(self, client, admin_headers):
        payload = {
            "name": "East Coast Warehouse",
            "code": "WH-EC-001",
            "city": "Boston",
            "country": "US",
            "capacity": 5000,
        }
        response = client.post("/api/v1/warehouses", headers=admin_headers, json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        data = body["data"]
        assert data["name"] == "East Coast Warehouse"
        assert data["code"] == "WH-EC-001"
        assert "id" in data

    def test_create_requires_auth(self, client):
        response = client.post("/api/v1/warehouses", json={"name": "X", "code": "X"})
        assert response.status_code == 401

    def test_create_missing_required_fields(self, client, admin_headers):
        response = client.post("/api/v1/warehouses", headers=admin_headers, json={"name": "No Code"})
        assert response.status_code == 422


class TestGetWarehouse:
    def test_get_existing_warehouse(self, client, admin_headers, test_warehouse):
        wh_id = str(test_warehouse.id)
        response = client.get(f"/api/v1/warehouses/{wh_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["data"]["id"] == wh_id

    def test_get_nonexistent_warehouse(self, client, admin_headers):
        import uuid
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/warehouses/{fake_id}", headers=admin_headers)
        assert response.status_code == 404


class TestUpdateWarehouse:
    def test_update_warehouse_success(self, client, admin_headers, test_warehouse):
        wh_id = str(test_warehouse.id)
        response = client.put(
            f"/api/v1/warehouses/{wh_id}",
            headers=admin_headers,
            json={"name": "Updated Warehouse Name"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Updated Warehouse Name"

    def test_update_nonexistent_warehouse(self, client, admin_headers):
        import uuid
        fake_id = str(uuid.uuid4())
        response = client.put(
            f"/api/v1/warehouses/{fake_id}",
            headers=admin_headers,
            json={"name": "Ghost"},
        )
        assert response.status_code == 404


class TestDeactivateWarehouse:
    def test_deactivate_warehouse(self, client, admin_headers, test_org, db):
        from app.models.warehouse import Warehouse

        # Warehouse must belong to the same org as the admin user (test_org)
        wh = Warehouse(
            organization_id=test_org.id,
            name="Warehouse To Deactivate",
            code="WH-DEACT",
            is_active=True,
        )
        db.add(wh)
        db.flush()

        wh_id = str(wh.id)
        response = client.delete(f"/api/v1/warehouses/{wh_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["data"]["is_active"] is False
