"""
API tests for /api/v1/orders endpoints.
Tests: list, create, get, update status.
"""
import pytest


class TestListOrders:
    def test_list_requires_auth(self, client):
        response = client.get("/api/v1/orders")
        assert response.status_code == 401

    def test_list_returns_paginated(self, client, admin_headers, test_order):
        response = client.get("/api/v1/orders", headers=admin_headers)
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert len(body["data"]) >= 1


class TestCreateOrder:
    def test_create_order_success(self, client, admin_headers, test_product):
        payload = {
            "reference_number": "ORD-API-TEST-001",
            "priority": "normal",
            "delivery_address": "456 Ship Lane",
            "items": [
                {
                    "product_id": str(test_product.id),
                    "quantity": 5.0,
                    "unit_price": 15.0,
                }
            ],
        }
        response = client.post("/api/v1/orders", headers=admin_headers, json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        data = body["data"]
        assert data["reference_number"] == "ORD-API-TEST-001"
        assert data["status"] == "pending"
        assert len(data["items"]) == 1

    def test_create_duplicate_reference_raises_conflict(self, client, admin_headers, test_order):
        payload = {
            "reference_number": test_order.reference_number,
            "items": [],
        }
        response = client.post("/api/v1/orders", headers=admin_headers, json=payload)
        assert response.status_code in (409, 422)

    def test_create_requires_auth(self, client):
        response = client.post("/api/v1/orders", json={})
        assert response.status_code == 401


class TestGetOrder:
    def test_get_existing_order(self, client, admin_headers, test_order):
        order_id = str(test_order.id)
        response = client.get(f"/api/v1/orders/{order_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["data"]["id"] == order_id

    def test_get_nonexistent_order(self, client, admin_headers):
        import uuid
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/orders/{fake_id}", headers=admin_headers)
        assert response.status_code == 404


class TestUpdateOrder:
    def test_update_order_status(self, client, admin_headers, test_order):
        order_id = str(test_order.id)
        response = client.patch(
            f"/api/v1/orders/{order_id}",
            headers=admin_headers,
            json={"status": "confirmed"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "confirmed"

    def test_update_nonexistent_order(self, client, admin_headers):
        import uuid
        fake_id = str(uuid.uuid4())
        response = client.patch(
            f"/api/v1/orders/{fake_id}",
            headers=admin_headers,
            json={"status": "confirmed"},
        )
        assert response.status_code == 404
