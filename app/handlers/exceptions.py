from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.config.settings import settings


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Exception do rate limiter."""
    retry_after = int(settings.RATE_LIMIT_WINDOW)

    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "retry_after_seconds": retry_after
        },
        headers={"Retry-After": str(retry_after)}
    )
