import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


# Get Env file
def get_env_file():
    env = os.getenv('ENVIRONMENT', 'development')
    if env == 'production':
        return '.env.prod'
    return '.env.dev'


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

    # Logs
    LOG_LEVEL: str

    # Token
    TOKEN: str

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding='utf-8'
    )


settings = Settings()
