"""
Seed script — creates initial system admin and demo organization.
Run once after applying migrations:
  python scripts/seed_data.py
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.organization import Organization
from app.models.user import User, UserRole


def seed() -> None:
    settings = get_settings()
    db = SessionLocal()

    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
        if existing:
            print(f"[seed] System admin already exists: {settings.FIRST_ADMIN_EMAIL}")
            return

        # Create default organization
        org = Organization(
            name="Default Organization",
            description="Auto-created organization for initial setup",
            contact_email=settings.FIRST_ADMIN_EMAIL,
        )
        db.add(org)
        db.flush()

        # Create system admin
        admin = User(
            email=settings.FIRST_ADMIN_EMAIL,
            full_name=settings.FIRST_ADMIN_FULL_NAME,
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            role=UserRole.SYSTEM_ADMIN,
            organization_id=org.id,
            is_active=True,
        )
        db.add(admin)
        db.commit()

        print(f"[seed] Created organization: '{org.name}' (id={org.id})")
        print(f"[seed] Created system admin: '{admin.email}' (id={admin.id})")
        print("[seed] Done. Change the admin password after first login.")

    except Exception as e:
        db.rollback()
        print(f"[seed] ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
