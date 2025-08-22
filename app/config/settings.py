import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


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

    PYTHONUNBUFFERED: Optional[str] = None

    BACKEND_HOST: Optional[str] = None  # Host do backend

    BACKEND_PORT: Optional[str] = None  # Porta do backend

    MODSEC_AUDIT_ENGINE: Optional[str] = None
    # Caminho do log de auditoria
    MODSEC_AUDIT_LOG: Optional[str] = None
    # Partes a serem logadas
    MODSEC_AUDIT_LOG_PARTS: Optional[str] = None
    # Tipo de log (Serial/Concurrent)
    MODSEC_AUDIT_LOG_TYPE: Optional[str] = None
    # Acesso ao corpo da requisição
    MODSEC_REQUEST_BODY_ACCESS: Optional[str] = None
    # Acesso ao corpo da resposta
    MODSEC_RESPONSE_BODY_ACCESS: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding='utf-8'
    )


settings = Settings()
