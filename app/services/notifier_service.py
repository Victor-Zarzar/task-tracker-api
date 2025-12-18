import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import Optional

import requests

from app.config.logger import logger
from app.config.settings import settings
from app.models.location import Location
from app.services.cache_service import is_already_notified, mark_notified


# Function to send email notification
def send_email_notification(
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
    if is_already_notified(visitor_ip, "email"):
        logger.info(f"Email already sent recently to IP {visitor_ip}. Ignoring.")
        return

    try:
        map_link = f"https://maps.google.com/?q={location.lat},{location.lon}"
        msg = EmailMessage()
        msg["Subject"] = "New visitor to your website!"
        msg["From"] = settings.EMAIL_ADDRESS
        msg["To"] = settings.EMAIL_ADDRESS

        msg.set_content(
            f"New visitor to your website!\n\n"
            f"Hello Victor,\n\n"
            f"A new visitor has accessed your website.\n\n"
            f"Details:\n"
            f"- IP: {visitor_ip}\n"
            f"Reason: {reason}\n"
            f"*Endpoint:* {endpoint or '-'}\n"
            f"*URL:* {url or '-'}\n"
            f"- User-Agent: {user_agent}\n"
            f"- Location: {location.city}, {location.region}, {location.country}\n"
            f"- Page: {page}\n"
            f"- Reference: {ref}\n"
            f"- Date and Time (UTC): {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"- See on map: {map_link}\n\n"
            f"Sincerely,\n"
            f"Tracker API"
        )

        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as smtp:
            smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)

        logger.info(
            f"Email sent — IP: {visitor_ip}, Page: {page}, Ref: {ref}, User-Agent: {user_agent}"
        )

        # Mark in cache
        mark_notified(visitor_ip, "email")

    except Exception as e:
        logger.error(f"Error sending email: {e}")


# Function to send Slack notification
def send_slack_notification(
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
    if is_already_notified(visitor_ip, "slack"):
        logger.info(f"Slack already recently notified for IP {visitor_ip}. Ignoring.")
        return

    try:
        map_link = f"https://maps.google.com/?q={location.lat},{location.lon}"

        webhook_url = settings.SLACK_WEBHOOK_URL

        text = (
            f"*New visitor to your website!*\n"
            f"*IP:* `{visitor_ip}`\n"
            f"Reason: {reason}\n"
            f"*Endpoint:* {endpoint or '-'}\n"
            f"*URL:* {url or '-'}\n"
            f"*Location:* {location.city}, {location.region}, {location.country}\n"
            f"*User-Agent:* {user_agent}\n"
            f"*Page:* {page}\n"
            f"*Reference:* {ref}\n"
            f"*Date/Time (UTC):* {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"*Map:* {map_link}"
        )

        data = {"text": text}

        response = requests.post(webhook_url, json=data)

        if response.status_code != 200:
            raise Exception(
                f"Slack webhook error: {response.status_code} - {response.text}"
            )
        logger.info(
            f"Slack notified — IP: {visitor_ip}, Page: {page}, Ref: {ref}, User-Agent: {user_agent}"
        )

        # Mark in cache
        mark_notified(visitor_ip, "slack")

    except Exception as e:
        logger.error(f"Slack error: {e}")
