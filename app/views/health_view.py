from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request

from app.config.logger import logger
from app.models.health import HealthCheckResponse
from app.services.auth_service import verify_token

router = APIRouter(prefix="/api/v1/tracker", tags=["Health Check"])


@router.get(
    "/health",
    summary="Health Check",
    description="Checks the status of the API and its dependencies",
    response_description="API status and dependencies",
    response_model=HealthCheckResponse,
)
async def health_check(
    request: Request,
    _: None = Depends(verify_token),
):
    start_time = datetime.now(timezone.utc)

    dependencies = {
        "api": "ok",
    }

    end_time = datetime.now(timezone.utc)
    response_time_ms = (end_time - start_time).total_seconds() * 1000

    logger.info(
        f"Health check performed - IP={request.client.host}, Time={response_time_ms:.2f}ms"
    )

    return {
        "status": "ok",
        "message": "API is running",
        "details": dependencies,
        "response_time_ms": round(response_time_ms, 2),
    }
