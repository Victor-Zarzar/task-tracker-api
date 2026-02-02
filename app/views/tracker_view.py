from fastapi import APIRouter, BackgroundTasks, Depends, Request

from app.config.logger import logger
from app.config.settings import settings
from app.models.check import CheckTracker
from app.schemas.tracker import TrackerSchema
from app.services.auth_service import verify_token
from app.services.request_context_service import collect_request_context
from app.tasks.tracker_tasks import notify_visitor_task

router = APIRouter(prefix="/api/v1", tags=["Tracker API"])


@router.get("/tracker", summary="Tracker", response_model=CheckTracker)
async def root(
    request: Request,
    background_tasks: BackgroundTasks,
    query: TrackerSchema = Depends(),
    _: None = Depends(verify_token),
):
    page = str(query.page)
    ctx = await collect_request_context(request)

    logger.info(
        f"Human visitor: {ctx['visitor_ip']} - {ctx['user_agent']} - page: {page}"
    )

    if settings.DEBUG:
        logger.warning("DEBUG mode active — notifications not sent.")
    else:
        background_tasks.add_task(
            notify_visitor_task,
            visitor_ip=ctx["visitor_ip"],
            page=page,
            location=ctx["location"],
            timestamp=ctx["timestamp"],
            user_agent=ctx["user_agent"],
            reason=ctx["reason"],
            endpoint=ctx["endpoint"],
            url=ctx["url"],
        )

    return CheckTracker(
        message="Website Tracker API - No Database Version",
        visitor_ip=ctx["visitor_ip"],
        user_agent=ctx["user_agent"],
        timestamp_utc=ctx["timestamp"],
        location=ctx["location"],
        page=page,
        url=ctx["url"],
        endpoint=ctx["endpoint"],
        status="debug" if settings.DEBUG else "notification sent",
        reason=ctx["reason"],
    )
