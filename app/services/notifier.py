import smtplib
from email.message import EmailMessage
from typing import Optional
import requests
from app.config.settings import settings


def send_email_notification(visitor_ip: str, page: str, ref: Optional[str]):
    """
    Sends an email notification informing the visitor's IP.
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = '🚀 Novo visitante no seu portfólio!'
        msg['From'] = settings.email_address
        msg['To'] = settings.email_address

        msg.set_content(
            f"Olá Victor,\n\n"
            f"Um novo visitante acessou seu portfólio.\n\n"
            f"Detalhes:\n"
            f"- IP do visitante: {visitor_ip}\n\n"
            f"Atenciosamente,\n"
            f"Seu Tracker API"
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(settings.email_address, settings.email_password)
            smtp.send_message(msg)

        print(
            f"📧 Enviando email para visita — IP: {visitor_ip}, Page: {page}, Ref: {ref}")

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")


def send_slack_notification(visitor_ip: str, page: str, ref: Optional[str]):
    """
    Sends a notification to a Slack channel via webhook.
    """
    try:
        webhook_url = settings.slack_webhook_url

        data = {
            "text": f":rocket: Novo visitante no portfólio!\n*IP:* `{visitor_ip}`"
        }

        response = requests.post(webhook_url, json=data)

        if response.status_code != 200:
            raise Exception(
                f"Erro Slack webhook: {response.status_code} - {response.text}"
            )

        print("✅ Notificação Slack enviada com sucesso!")

    except Exception as e:
        print(f"💬 Enviando Slack — IP: {visitor_ip}, Page: {page}, Ref: {ref}")
