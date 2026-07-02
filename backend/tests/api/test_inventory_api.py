"""
API tests for /api/v1/inventory endpoints.
Tests: list, set inventory, get item, adjust, low-stock alerts.
"""
import pytest


class TestListInventory:
    def test_list_requires_auth(self, client):
        response = client.get("/api/v1/inventory")
        assert response.status_code == 401

    def test_list_returns_items(self, client, admin_headers, test_inventory):
        response = client.get("/api/v1/inventory", headers=admin_headers)
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert len(body["data"]) >= 1


class TestSetInventory:
    def test_create_inventory_entry(self, client, admin_headers, db):
        from app.models.organization import Organization
        from app.models.warehouse import Warehouse
        from app.models.product import Product

        org = Organization(name="Inv Create Org", is_active=True)
        db.add(org)
        db.flush()

        wh = Warehouse(
            organization_id=org.id, name="Inv WH", code="INV-WH-01", is_active=True
        )
        db.add(wh)
        db.flush()

        prod = Product(
            organization_id=org.id,
            name="Inv Product",
            sku="INV-SKU-001",
            unit="unit",
            is_active=True,
        )
        db.add(prod)
        db.flush()

        payload = {
            "product_id": str(prod.id),
            "warehouse_id": str(wh.id),
            "quantity_on_hand": 150.0,
            "reorder_point": 25.0,
            "safety_stock": 10.0,
        }
        response = client.post("/api/v1/inventory", headers=admin_headers, json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert body["data"]["quantity_on_hand"] == 150.0

    def test_create_requires_auth(self, client):
        response = client.post("/api/v1/inventory", json={})
        assert response.status_code == 401


class TestGetInventoryItem:
    def test_get_existing_item(self, client, admin_headers, test_inventory):
        item_id = str(test_inventory.id)
        response = client.get(f"/api/v1/inventory/{item_id}", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == item_id
        assert data["quantity_on_hand"] == 100.0

    def test_get_nonexistent_item(self, client, admin_headers):
        import uuid
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/inventory/{fake_id}", headers=admin_headers)
        assert response.status_code == 404


class TestAdjustInventory:
    def test_adjust_positive_delta(self, client, admin_headers, test_inventory):
        item_id = str(test_inventory.id)
        response = client.post(
            f"/api/v1/inventory/{item_id}/adjust",
            headers=admin_headers,
            json={"delta": 50.0},
        )
        assert response.status_code == 200
        assert response.json()["data"]["quantity_on_hand"] == 150.0

    def test_adjust_negative_delta(self, client, admin_headers, test_inventory):
        # Each test gets a fresh DB snapshot (100.0 on hand).
        # Adjust by -30 → 70.0
        item_id = str(test_inventory.id)
        response = client.post(
            f"/api/v1/inventory/{item_id}/adjust",
            headers=admin_headers,
            json={"delta": -30.0},
        )
        assert response.status_code == 200
        assert response.json()["data"]["quantity_on_hand"] == 70.0


class TestLowStockAlerts:
    def test_low_stock_endpoint(self, client, admin_headers, db):
        from app.models.organization import Organization
        from app.models.warehouse import Warehouse
        from app.models.product import Product
        from app.models.inventory import InventoryItem

        org = Organization(name="Low Stock Org", is_active=True)
        db.add(org)
        db.flush()

        wh = Warehouse(
            organization_id=org.id, name="LS WH", code="LS-WH-01", is_active=True
        )
        db.add(wh)
        db.flush()

        prod = Product(
            organization_id=org.id,
            name="Low Stock Product",
            sku="LS-SKU-001",
            unit="unit",
            is_active=True,
        )
        db.add(prod)
        db.flush()

        # qty below reorder point → triggers alert
        item = InventoryItem(
            product_id=prod.id,
            warehouse_id=wh.id,
            quantity_on_hand=5.0,
            quantity_reserved=0.0,
            reorder_point=20.0,
        )
        db.add(item)
        db.flush()

        response = client.get("/api/v1/inventory/alerts/low-stock", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
