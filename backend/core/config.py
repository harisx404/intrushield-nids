"""Application configuration loaded from environment variables."""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All application settings loaded from .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "NIDS-Pro"
    APP_ENV: Literal["development", "production", "testing"] = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False

    # ── Security ─────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = Field(
        ..., description="256-bit random key — CHANGE IN PRODUCTION"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./database/nids.db"

    # ── Suricata ─────────────────────────────────────────────────────────
    SURICATA_LOG_PATH: str = "/var/log/suricata/eve.json"
    SURICATA_CONFIG_PATH: str = "/etc/suricata/suricata.yaml"
    SURICATA_RULES_PATH: str = "/etc/suricata/rules/custom.rules"
    SURICATA_BINARY: str = "suricata"

    # ── GeoIP ────────────────────────────────────────────────────────────
    GEOIP_DB_PATH: str = "/opt/geoip/GeoLite2-City.mmdb"

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:3000"

    # ── Rate Limiting ────────────────────────────────────────────────────
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # ── Response Engine ──────────────────────────────────────────────────
    ENABLE_LOG_RESPONSE: bool = True
    ENABLE_EMAIL_RESPONSE: bool = False
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    ALERT_EMAIL_TO: str = ""
    EMAIL_MIN_SEVERITY: str = "HIGH"

    ENABLE_WEBHOOK_RESPONSE: bool = False
    WEBHOOK_URL: str = ""
    WEBHOOK_MIN_SEVERITY: str = "MEDIUM"

    ENABLE_FIREWALL_RESPONSE: bool = False
    ENABLE_IP_BLOCK_RESPONSE: bool = False
    IP_BLOCK_THRESHOLD_COUNT: int = 5
    IP_BLOCK_THRESHOLD_MINUTES: int = 5
    IP_BLOCK_DURATION_HOURS: int = 24

    def get_cors_origins(self) -> list[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Ensure JWT secret is not a placeholder value."""
        if v in ("CHANGE_ME", "changeme", "secret", ""):
            raise ValueError("JWT_SECRET_KEY must be set to a secure random value")
        return v


settings = Settings()
