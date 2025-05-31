from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "message": f"Você atingiu o limite de {exc.detail}. Tente novamente mais tarde.",
            "retry_after_seconds": 60
        }
    )
