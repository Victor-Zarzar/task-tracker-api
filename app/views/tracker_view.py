from fastapi import APIRouter
from app.services.rate_limiter import limiter
from app.config.settings import settings

router = APIRouter(prefix="/tracker", tags=["Tracker API"])


@router.get("/")
@limiter.limit("5/minute")
async def root():
    return {
        "message": "Portfolio Tracker API - No Database Version",
        "version": "1.0.0",
        "status": "active",
        "environment": settings.environment,
        "features": [...]
    }
