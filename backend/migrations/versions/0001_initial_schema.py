"""Initial schema — all tables

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # ENUMS
    # ------------------------------------------------------------------ #
    op.execute("CREATE TYPE user_role AS ENUM ('system_admin','org_admin','warehouse_manager','inventory_manager','operations_manager')")
    op.execute("CREATE TYPE order_status AS ENUM ('pending','confirmed','allocated','in_progress','shipped','delivered','cancelled')")
    op.execute("CREATE TYPE order_priority AS ENUM ('low','normal','high','urgent')")

    # ------------------------------------------------------------------ #
    # ORGANIZATIONS
    # ------------------------------------------------------------------ #
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(50), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_organizations_name", "organizations", ["name"], unique=True)

    # ------------------------------------------------------------------ #
    # USERS
    # ------------------------------------------------------------------ #
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", postgresql.ENUM("system_admin","org_admin","warehouse_manager","inventory_manager","operations_manager", name="user_role", create_type=False), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_organization_id", "users", ["organization_id"])

    # ------------------------------------------------------------------ #
    # WAREHOUSES
    # ------------------------------------------------------------------ #
    op.create_table(
        "warehouses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("latitude", sa.Float, nullable=True),
        sa.Column("longitude", sa.Float, nullable=True),
        sa.Column("capacity", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_warehouses_organization_id", "warehouses", ["organization_id"])
    op.create_index("ix_warehouses_name", "warehouses", ["name"])

    # ------------------------------------------------------------------ #
    # PRODUCTS
    # ------------------------------------------------------------------ #
    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("sku", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("unit", sa.String(50), nullable=False, server_default="unit"),
        sa.Column("unit_cost", sa.Float, nullable=True),
        sa.Column("unit_price", sa.Float, nullable=True),
        sa.Column("reorder_point", sa.Float, nullable=True),
        sa.Column("lead_time_days", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_products_organization_id", "products", ["organization_id"])
    op.create_index("ix_products_name", "products", ["name"])
    op.create_index("ix_products_sku", "products", ["sku"])
    op.create_index("ix_products_category", "products", ["category"])

    # ------------------------------------------------------------------ #
    # INVENTORY ITEMS
    # ------------------------------------------------------------------ #
    op.create_table(
        "inventory_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("quantity_on_hand", sa.Float, nullable=False, server_default="0"),
        sa.Column("quantity_reserved", sa.Float, nullable=False, server_default="0"),
        sa.Column("reorder_point", sa.Float, nullable=True),
        sa.Column("safety_stock", sa.Float, nullable=True),
        sa.Column("last_counted_at", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("product_id", "warehouse_id", name="uq_inventory_product_warehouse"),
    )
    op.create_index("ix_inventory_product_id", "inventory_items", ["product_id"])
    op.create_index("ix_inventory_warehouse_id", "inventory_items", ["warehouse_id"])

    # ------------------------------------------------------------------ #
    # ORDERS
    # ------------------------------------------------------------------ #
    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("reference_number", sa.String(100), nullable=False),
        sa.Column("status", postgresql.ENUM("pending","confirmed","allocated","in_progress","shipped","delivered","cancelled", name="order_status", create_type=False), nullable=False, server_default="pending"),
        sa.Column("priority", postgresql.ENUM("low","normal","high","urgent", name="order_priority", create_type=False), nullable=False, server_default="normal"),
        sa.Column("delivery_address", sa.Text, nullable=True),
        sa.Column("delivery_latitude", sa.Float, nullable=True),
        sa.Column("delivery_longitude", sa.Float, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("total_amount", sa.Float, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_orders_organization_id", "orders", ["organization_id"])
    op.create_index("ix_orders_reference_number", "orders", ["reference_number"], unique=True)
    op.create_index("ix_orders_status", "orders", ["status"])

    # ------------------------------------------------------------------ #
    # ORDER ITEMS
    # ------------------------------------------------------------------ #
    op.create_table(
        "order_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantity", sa.Float, nullable=False),
        sa.Column("unit_price", sa.Float, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_product_id", "order_items", ["product_id"])

    # ------------------------------------------------------------------ #
    # WAREHOUSE ALLOCATION RESULTS
    # ------------------------------------------------------------------ #
    op.create_table(
        "warehouse_allocation_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("coverage_percentage", sa.Float, nullable=True),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("allocation_details", postgresql.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_war_order_id", "warehouse_allocation_results", ["order_id"])
    op.create_index("ix_war_warehouse_id", "warehouse_allocation_results", ["warehouse_id"])

    # ------------------------------------------------------------------ #
    # DEMAND FORECASTS
    # ------------------------------------------------------------------ #
    op.create_table(
        "demand_forecasts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("warehouses.id", ondelete="SET NULL"), nullable=True),
        sa.Column("forecast_method", sa.String(100), nullable=False),
        sa.Column("forecast_horizon_days", sa.Integer, nullable=False),
        sa.Column("forecast_data", postgresql.JSON, nullable=False),
        sa.Column("confidence", sa.Float, nullable=True),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_demand_forecasts_product_id", "demand_forecasts", ["product_id"])

    # ------------------------------------------------------------------ #
    # INVENTORY RECOMMENDATIONS
    # ------------------------------------------------------------------ #
    op.create_table(
        "inventory_recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("safety_stock", sa.Float, nullable=True),
        sa.Column("reorder_point", sa.Float, nullable=True),
        sa.Column("recommended_order_quantity", sa.Float, nullable=True),
        sa.Column("expected_holding_cost", sa.Float, nullable=True),
        sa.Column("expected_shortage_risk", sa.Float, nullable=True),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_inv_rec_product_id", "inventory_recommendations", ["product_id"])
    op.create_index("ix_inv_rec_warehouse_id", "inventory_recommendations", ["warehouse_id"])

    # ------------------------------------------------------------------ #
    # ROUTE OPTIMIZATION RESULTS
    # ------------------------------------------------------------------ #
    op.create_table(
        "route_optimization_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reference", sa.String(100), nullable=True),
        sa.Column("route_data", postgresql.JSON, nullable=False),
        sa.Column("total_distance_km", sa.Float, nullable=True),
        sa.Column("estimated_duration_minutes", sa.Integer, nullable=True),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_route_opt_org_id", "route_optimization_results", ["organization_id"])

    # ------------------------------------------------------------------ #
    # ACTIVITY LOGS
    # ------------------------------------------------------------------ #
    op.create_table(
        "activity_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=True),
        sa.Column("resource_id", sa.String(100), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("metadata", postgresql.JSON, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_activity_logs_user_id", "activity_logs", ["user_id"])
    op.create_index("ix_activity_logs_organization_id", "activity_logs", ["organization_id"])
    op.create_index("ix_activity_logs_action", "activity_logs", ["action"])


def downgrade() -> None:
    op.drop_table("activity_logs")
    op.drop_table("route_optimization_results")
    op.drop_table("inventory_recommendations")
    op.drop_table("demand_forecasts")
    op.drop_table("warehouse_allocation_results")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("inventory_items")
    op.drop_table("products")
    op.drop_table("warehouses")
    op.drop_table("users")
    op.drop_table("organizations")
    op.execute("DROP TYPE IF EXISTS order_priority")
    op.execute("DROP TYPE IF EXISTS order_status")
    op.execute("DROP TYPE IF EXISTS user_role")
