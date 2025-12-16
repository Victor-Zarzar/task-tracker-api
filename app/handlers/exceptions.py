from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.config.settings import settings


# Exception handler for rate limiting
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    retry_after = int(settings.RATE_LIMIT_WINDOW)

    return JSONResponse(
        status_code=429,
        content={"error": "Too Many Requests", "retry_after_seconds": retry_after},
        headers={"Retry-After": str(retry_after)},
    )
