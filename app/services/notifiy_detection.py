from datetime import datetime

from app.config.logger import logger
from app.models.location import Location
from app.services.cache_service import is_already_notified, mark_notified
from app.services.notifier_service import (
    send_email_notification,
    send_slack_notification,
)


def notify_tracker_detection(
    visitor_ip: str,
    location: Location,
    timestamp: datetime,
    user_agent: str,
    reason: str,
    endpoint: str,
    url: str,
    page: str,
    ref: str,
):
    """Send notification to Slack and Email if not already sent"""

    # Slack
    if not is_already_notified(visitor_ip, "slack"):
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
        mark_notified(visitor_ip, "slack")
    else:
        logger.info(f"Slack notification already sent to IP {visitor_ip}")

    # Email
    if not is_already_notified(visitor_ip, "email"):
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
        mark_notified(visitor_ip, "email")
    else:
        logger.info(f"Email notification already sent to IP {visitor_ip}")
