from datetime import datetime
from typing import Optional

from app.config.logger import logger
from app.models.location import Location
from app.services.notifier_service import (
    send_email_notification,
    send_slack_notification,
)


def notify_visitor_task(
    *,
    visitor_ip: str,
    page: str,
    ref: Optional[str],
    location: Location,
    timestamp: datetime,
    user_agent: str,
    reason: str,
    endpoint: str,
    url: str,
):
    """
    Background task responsible for notifying visitor access.
    """
    try:
        send_email_notification(
            visitor_ip=visitor_ip,
            page=page,
            ref=ref,
            location=location,
            timestamp=timestamp,
            user_agent=user_agent,
            reason=reason,
            endpoint=endpoint,
            url=url,
        )

        send_slack_notification(
            visitor_ip=visitor_ip,
            page=page,
            ref=ref,
            location=location,
            timestamp=timestamp,
            user_agent=user_agent,
            reason=reason,
            endpoint=endpoint,
            url=url,
        )

    except Exception as exc:
        logger.error(f"Error executing notify_visitor_task: {exc}")
