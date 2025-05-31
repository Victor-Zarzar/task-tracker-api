from fastapi import APIRouter, Request
from app.services.rate_limiter import limiter
from app.config.settings import settings

router = APIRouter(prefix="/tracker", tags=["Tracker API"])


@router.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {
        "message": "Portfolio Tracker API - No Database Version",
        "version": "1.0.0",
        "status": "active",
        "environment": settings.environment,
        "features": [
            "In-memory tracking",
            "Email notifications",
            "Slack notifications",
            "Bot filtering"
        ]
    }
