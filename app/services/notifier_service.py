from datetime import datetime
import smtplib
from email.message import EmailMessage
from typing import Optional
import requests
from app.logger import logger
from app.config.settings import settings
from app.models.tracker_model import Location
from cachetools import TTLCache

notification_cache = TTLCache(maxsize=500, ttl=300)


def is_already_notified(visitor_ip: str, channel: str) -> bool:
    """
    Returns True if we have already sent a notification to this IP on the specified channel.
    """
    key = f"{channel}:{visitor_ip}"
    return key in notification_cache


def mark_notified(visitor_ip: str, channel: str):
    """
    Marks the IP as already notified in the channel.
    """
    key = f"{channel}:{visitor_ip}"
    notification_cache[key] = True


def send_email_notification(visitor_ip: str, page: str, ref: Optional[str], location: Location, timestamp: datetime, user_agent: str):
    if is_already_notified(visitor_ip, "email"):
        logger.info(
            f"⏳ Email already sent recently to IP {visitor_ip}. Ignoring.")
        return

    try:
        lat, lon = (location.loc.split(",") if location.loc else ("", ""))
        map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}" if lat and lon else "Map unavailable"

        msg = EmailMessage()
        msg['Subject'] = '🚀 New visitor to your website!'
        msg['From'] = settings.email_address
        msg['To'] = settings.email_address

        msg.set_content(
            f"🚀 New visitor to your website!\n\n"
            f"Hello Victor,\n\n"
            f"A new visitor has accessed your website.\n\n"
            f"Detalhes:\n"
            f"- IP: {visitor_ip}\n"
            f"- User-Agent: {user_agent}\n"
            f"- Location: {location.city}, {location.region}, {location.country}\n"
            f"- Page: {page}\n"
            f"- Reference: {ref}\n"
            f"- Date and Time (UTC): {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"- 🗺️ See on map: {map_link}\n\n"
            f"Sincerely,\n"
            f"Tracker API"
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(settings.email_address, settings.email_password)
            smtp.send_message(msg)

        logger.info(
            f"📧 Email sent — IP: {visitor_ip}, Page: {page}, Ref: {ref}, User-Agent: {user_agent}")

        # Marca no cache
        mark_notified(visitor_ip, "email")

    except Exception as e:
        logger.error(
            f"Error sending email: {e}")


def send_slack_notification(visitor_ip: str, page: str, ref: Optional[str], location: Location, timestamp: datetime, user_agent: str):
    if is_already_notified(visitor_ip, "slack"):
        logger.info(
            f"⏳ Slack already recently notified for IP {visitor_ip}. Ignoring.")
        return

    try:
        lat, lon = (location.loc.split(",") if location.loc else ("", ""))
        map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}" if lat and lon else "Map unavailable"

        webhook_url = settings.slack_webhook_url

        text = (
            f":rocket: *New visitor to your website!*\n"
            f"*IP:* `{visitor_ip}`\n"
            f"*Location:* {location.city}, {location.region}, {location.country}\n"
            f"*User-Agent:* {user_agent}\n"
            f"*Page:* {page}\n"
            f"*Reference:* {ref}\n"
            f"*Date/Time (UTC):* {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"*🗺️ Map:* {map_link}"
        )

        data = {"text": text}

        response = requests.post(webhook_url, json=data)

        if response.status_code != 200:
            raise Exception(
                f"Slack webhook error: {response.status_code} - {response.text}"
            )
        logger.info(
            f"Slack notified — IP: {visitor_ip}, Page: {page}, Ref: {ref}, User-Agent: {user_agent}")

        # Mark in cache
        mark_notified(visitor_ip, "slack")

    except Exception as e:
        logger.error(f"Slack error: {e}")
