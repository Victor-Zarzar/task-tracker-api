import os
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file():
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ".env.prod"
    return ".env.dev"


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    ENVIRONMENT: str
    APP_DOMAIN: Optional[str] = None
    SSL_EMAIL: Optional[str] = None

    ALLOWED_ORIGINS: List[str]

    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    SLACK_WEBHOOK_URL: str

    LOG_LEVEL: str

    TOKEN: str

    ENABLE_RATE_LIMITER: bool = False
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW: int

    PYTHONUNBUFFERED: Optional[str] = None
    BACKEND_HOST: Optional[str] = None
    BACKEND_PORT: Optional[str] = None

    MODSEC_AUDIT_ENGINE: Optional[str] = None
    MODSEC_AUDIT_LOG: Optional[str] = None
    MODSEC_AUDIT_LOG_PARTS: Optional[str] = None
    MODSEC_AUDIT_LOG_TYPE: Optional[str] = None
    MODSEC_REQUEST_BODY_ACCESS: Optional[str] = None
    MODSEC_RESPONSE_BODY_ACCESS: Optional[str] = None

    LOKI_HTTP_PORT: Optional[int] = None
    LOKI_GRPC_PORT: Optional[int] = None
    LOKI_RETENTION_PERIOD: Optional[str] = None
    LOKI_DATA_PATH: Optional[str] = None

    PROMTAIL_HTTP_PORT: Optional[int] = None
    PROMTAIL_POSITIONS_FILE: Optional[str] = None
    LOKI_URL: Optional[str] = None

    GRAFANA_PORT: Optional[int] = None
    GRAFANA_ADMIN_USER: Optional[str] = None
    GRAFANA_ADMIN_PASSWORD: Optional[str] = None
    GRAFANA_DOMAIN: Optional[str] = None
    GRAFANA_ROOT_URL: Optional[str] = None

    NGINX_LOG_PATH: Optional[str] = None
    MODSEC_LOG_PATH: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=get_env_file(), env_file_encoding="utf-8"
    )


settings = Settings()
