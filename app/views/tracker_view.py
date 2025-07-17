from typing import Optional
from app.logger import logger
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, status, Query, Depends
from app.services.notifier_service import send_email_notification, send_slack_notification
from datetime import datetime, timezone
from app.models.tracker_model import CheckTracker, Location
from app.services.auth_service import verify_token
import httpx


router = APIRouter(prefix="/api/v1", tags=["Tracker API"])


# Get location based on IP
async def get_location(ip: str) -> Location:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipinfo.io/{ip}/json")
            if response.status_code == 200:
                data = response.json()
                return Location(
                    city=data.get("city"),
                    region=data.get("region"),
                    country=data.get("country"),
                    loc=data.get("loc")
                )
    except Exception as e:
        logger.error(
            f"Error fetching location: {e}")
    return Location()


# Route for tracker
@router.get("/tracker",
            summary="Tracker",
            description="Performs the task of sending notification",
            response_description="Status da API e dependências",
            response_model=CheckTracker)
async def root(
    request: Request,
    background_tasks: BackgroundTasks,
    page: str = Query(default="Website"),
    ref: Optional[str] = Query(
        default=None, description="Referrer or campaign"),
    debug: bool = Query(default=False, description="Enable debug mode"),
    _: None = Depends(verify_token)
):
    visitor_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    timestamp = datetime.now(timezone.utc)

    location = await get_location(visitor_ip)

    logger.info(
        f"Human visitor: {visitor_ip} - {user_agent} - page: {page} - ref: {ref}")

    if not debug:
        background_tasks.add_task(
            send_email_notification, visitor_ip, page, ref, location, timestamp, user_agent)
        background_tasks.add_task(
            send_slack_notification, visitor_ip, page, ref, location, timestamp, user_agent)
    else:
        logger.warning(
            "Debug mode active — notifications not sent.")

    # Return response
    return CheckTracker(
        message="Website Tracker API - No Database Version",
        visitor_ip=visitor_ip,
        user_agent=user_agent,
        timestamp_utc=timestamp,
        location=location,
        status="notification sent (debug)" if debug else "notification sent",
    )
