import os

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
    APP_DOMAIN: str | None = None
    SSL_EMAIL: str | None = None

    ALLOWED_ORIGINS: list[str]

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

    PYTHONUNBUFFERED: str | None = None
    BACKEND_HOST: str | None = None
    BACKEND_PORT: str | None = None

    MODSEC_AUDIT_ENGINE: str | None = None
    MODSEC_AUDIT_LOG: str | None = None
    MODSEC_AUDIT_LOG_PARTS: str | None = None
    MODSEC_AUDIT_LOG_TYPE: str | None = None
    MODSEC_REQUEST_BODY_ACCESS: str | None = None
    MODSEC_RESPONSE_BODY_ACCESS: str | None = None

    LOKI_HTTP_PORT: int | None = None
    LOKI_GRPC_PORT: int | None = None
    LOKI_RETENTION_PERIOD: str | None = None
    LOKI_DATA_PATH: str | None = None

    PROMTAIL_HTTP_PORT: int | None = None
    PROMTAIL_POSITIONS_FILE: str | None = None
    LOKI_URL: str | None = None

    GRAFANA_PORT: int | None = None
    GRAFANA_ADMIN_USER: str | None = None
    GRAFANA_ADMIN_PASSWORD: str | None = None
    GRAFANA_DOMAIN: str | None = None
    GRAFANA_ROOT_URL: str | None = None

    NGINX_LOG_PATH: str | None = None
    MODSEC_LOG_PATH: str | None = None

    model_config = SettingsConfigDict(
        env_file=get_env_file(), env_file_encoding="utf-8"
    )


settings = Settings()
