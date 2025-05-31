from datetime import datetime
import smtplib
from email.message import EmailMessage
from typing import Optional
import requests
from app.config.settings import settings
from app.models.tracker_model import Location


def send_email_notification(visitor_ip: str, page: str, ref: Optional[str], location: Location, timestamp: datetime, user_agent: str):
    try:
        lat, lon = (location.loc.split(",") if location.loc else ("", ""))
        map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}" if lat and lon else "Mapa indisponível"

        msg = EmailMessage()
        msg['Subject'] = '🚀 Novo visitante no seu Website!'
        msg['From'] = settings.email_address
        msg['To'] = settings.email_address

        msg.set_content(
            f"🚀 Novo visitante no seu Website!\n\n"
            f"Olá Victor,\n\n"
            f"Um novo visitante acessou seu Website.\n\n"
            f"Detalhes:\n"
            f"- IP: {visitor_ip}\n"
            f"- User-Agent: {user_agent}\n"
            f"- Localização: {location.city}, {location.region}, {location.country}\n"
            f"- Página: {page}\n"
            f"- Referência: {ref}\n"
            f"- Data e Hora (UTC): {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"- 🗺️ Ver no mapa: {map_link}\n\n"
            f"Atenciosamente,\n"
            f"Tracker API"
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(settings.email_address, settings.email_password)
            smtp.send_message(msg)

        print(
            f"📧 Email enviado — IP: {visitor_ip}, Page: {page}, Ref: {ref}, User-Agent: {user_agent}")

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")


def send_slack_notification(visitor_ip: str, page: str, ref: Optional[str], location: Location, timestamp: datetime, user_agent: str):
    try:
        lat, lon = (location.loc.split(",") if location.loc else ("", ""))
        map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}" if lat and lon else "Mapa indisponível"

        webhook_url = settings.slack_webhook_url

        text = (
            f":rocket: *Novo visitante no seu Website!*\n"
            f"*IP:* `{visitor_ip}`\n"
            f"*Localização:* {location.city}, {location.region}, {location.country}\n"
            f"*User-Agent:* {user_agent}\n"
            f"*Página:* {page}\n"
            f"*Referência:* {ref}\n"
            f"*Data/Hora (UTC):* {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"*🗺️ Mapa:* {map_link}"
        )

        data = {"text": text}

        response = requests.post(webhook_url, json=data)

        if response.status_code != 200:
            raise Exception(
                f"Erro Slack webhook: {response.status_code} - {response.text}"
            )

        print(
            f"✅ Slack notificado — IP: {visitor_ip}, Page: {page}, Ref: {ref}, User-Agent: {user_agent}")

    except Exception as e:
        print(f"❌ Erro Slack: {e}")
