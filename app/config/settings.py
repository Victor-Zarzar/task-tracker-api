from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW: int

    # App Info
    APP_NAME: str
    DEBUG: bool
    ENVIRONMENT: str

    # CORS
    ALLOWED_ORIGINS: List[str]

    # Email
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    # Slack
    SLACK_WEBHOOK_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
