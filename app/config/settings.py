from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Rate Limiting
    rate_limit_requests: int = 5
    rate_limit_window: int = 60

    # App Info
    app_name: str = "Portfolio Tracker"
    debug: bool = False
    environment: str = "development"

    # CORS
    allowed_origins: List[str] = ["*"]

    # Email
    email_address: str
    email_password: str
    smtp_server: str
    smtp_port: int

    class Config:
        env_file = ".env"


settings = Settings()
