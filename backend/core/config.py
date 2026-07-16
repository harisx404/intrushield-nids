from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    APP_ENV: Literal["development", "production", "testing"] = Field("development")
    APP_NAME: str = "NIDS-Pro"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False
    
    JWT_SECRET_KEY: str = Field(...)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DATABASE_URL: str = Field(...)
    
    SURICATA_LOG_PATH: str = "/var/log/suricata/eve.json"
    SURICATA_CONFIG_PATH: str = "/etc/suricata/suricata.yaml"
    SURICATA_RULES_PATH: str = "/etc/suricata/rules/custom.rules"
    GEOIP_DB_PATH: Optional[str] = None
    CORS_ORIGINS: str = "http://localhost:3000"
    
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

settings = Settings()
