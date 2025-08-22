from typing import Optional
from app.config.logger import logger
from app.services.request_context_service import collect_request_context
from fastapi import APIRouter, Request, BackgroundTasks, Query, Depends
from app.services.notifier_service import send_email_notification, send_slack_notification
from app.models.tracker_model import CheckTracker
from app.services.auth_service import verify_token


router = APIRouter(prefix="/api/v1", tags=["Tracker API"])


# Route for tracker
@router.get("/tracker", summary="Tracker", response_model=CheckTracker)
async def root(
    request: Request,
    background_tasks: BackgroundTasks,
    page: str = Query(default="Website"),
    ref: Optional[str] = Query(
        default=None, description="Referrer or campaign"),
    debug: bool = Query(default=False, description="Enable debug mode"),
    _: None = Depends(verify_token)
):
    ctx = await collect_request_context(request)

    logger.info(
        f"Human visitor: {ctx['visitor_ip']} - {ctx['user_agent']} - page: {page} - ref: {ref}")

    if not debug:
        background_tasks.add_task(
            send_email_notification, ctx["visitor_ip"], page, ref, ctx["location"], ctx[
                "timestamp"], ctx["user_agent"], ctx["endpoint"], ctx["url"]
        )
        background_tasks.add_task(
            send_slack_notification, ctx["visitor_ip"], page, ref, ctx["location"], ctx[
                "timestamp"], ctx["user_agent"], ctx["endpoint"], ctx["url"]
        )
    else:
        logger.warning("Debug mode active — notifications not sent.")

    return CheckTracker(
        message="Website Tracker API - No Database Version",
        visitor_ip=ctx["visitor_ip"],
        user_agent=ctx["user_agent"],
        timestamp_utc=ctx["timestamp"],
        location=ctx["location"],
        url=ctx["url"],
        endpoint=ctx["endpoint"],
        status="notification sent (debug)" if debug else "notification sent",
    )
