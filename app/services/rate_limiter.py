from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        f"{settings.rate_limit_requests}/{settings.rate_limit_window} seconds"]
)
