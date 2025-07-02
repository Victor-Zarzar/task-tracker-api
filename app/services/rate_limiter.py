from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config.settings import settings

limit_string = f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_WINDOW} second"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[limit_string]
)
