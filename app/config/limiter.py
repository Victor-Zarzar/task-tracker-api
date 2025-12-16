from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config.logger import logger
from app.handlers.exceptions import rate_limit_exceeded_handler
from app.services.rate_limiter import limiter


def setup_rate_limiter(app: FastAPI, enabled: bool = True) -> None:
    """
    Configures the rate limiter in the FastAPI application.
    """
    if not enabled:
        logger.info("Rate limiter disabled by configuration")
        return

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    logger.info("Rate limiter configured and active")
