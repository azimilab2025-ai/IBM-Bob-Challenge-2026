"""
Application configuration loaded from environment variables.
All settings are validated at startup. No defaults for secrets.
"""
from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -----------------------------------------------------------------------
    # Application
    # -----------------------------------------------------------------------
    APP_NAME: str = "Supply Chain Optimization Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # -----------------------------------------------------------------------
    # Server
    # -----------------------------------------------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -----------------------------------------------------------------------
    # Database
    # -----------------------------------------------------------------------
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # -----------------------------------------------------------------------
    # Authentication
    # -----------------------------------------------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -----------------------------------------------------------------------
    # CORS
    # -----------------------------------------------------------------------
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    # -----------------------------------------------------------------------
    # Initial seed data
    # -----------------------------------------------------------------------
    FIRST_ADMIN_EMAIL: str = "admin@example.com"
    FIRST_ADMIN_PASSWORD: str = "ChangeMe123!"
    FIRST_ADMIN_FULL_NAME: str = "System Administrator"

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_must_be_strong(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance. Call once per process."""
    return Settings()
