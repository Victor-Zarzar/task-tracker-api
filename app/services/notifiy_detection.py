from datetime import datetime
from app.services.notifier_service import send_slack_notification, send_email_notification
from app.services.cache_service import is_already_notified, mark_notified
from app.models.tracker_model import Location
from app.config.logger import logger


def notify_tracker_detection(
    visitor_ip: str,
    location: Location,
    timestamp: datetime,
    user_agent: str,
    reason: str,
    endpoint: str,
    url: str,
    page: str,
    ref: str
):
    """Send notification to Slack if not already sent"""
    if is_already_notified(visitor_ip, "slack"):
        logger.info(f"⏳ Notification already sent to IP {visitor_ip}")
        return

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
