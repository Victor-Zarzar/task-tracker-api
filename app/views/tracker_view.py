from typing import Optional
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, status, Query
from app.services.rate_limiter import limiter
from app.services.notifier import send_email_notification, send_slack_notification
from datetime import datetime, timezone
from app.models.tracker_model import CheckTracker, Location
import httpx


router = APIRouter(prefix="/api/v1/tracker", tags=["Tracker API"])


BOT_USER_AGENTS = [
    "Googlebot", "Bingbot", "Slurp", "DuckDuckBot", "Baiduspider",
    "YandexBot", "Sogou", "Exabot", "facebot", "ia_archiver"
]


def is_bot(user_agent: str) -> bool:
    if user_agent:
        user_agent_lower = user_agent.lower()
        return any(bot.lower() in user_agent_lower for bot in BOT_USER_AGENTS)
    return False


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
        print(f"⚠️ Erro ao buscar localização: {e}")
    return Location()


@router.get("/", response_model=CheckTracker)
@limiter.limit("1/minute")
async def root(
    request: Request,
    background_tasks: BackgroundTasks,
    page: str = Query(default="Website"),
    ref: Optional[str] = Query(
        default=None, description="Referrer or campaign"),
    debug: bool = Query(default=False, description="Enable debug mode")
):
    visitor_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    timestamp = datetime.now(timezone.utc)

    if is_bot(user_agent):
        print(f"🤖 Bot detectado: {user_agent} - IP: {visitor_ip}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bots não são permitidos."
        )

    location = await get_location(visitor_ip)

    print(
        f"👤 Visitante humano: {visitor_ip} - {user_agent} - page: {page} - ref: {ref}")

    if not debug:
        background_tasks.add_task(
            send_email_notification, visitor_ip, page, ref, location, timestamp, user_agent)
        background_tasks.add_task(
            send_slack_notification, visitor_ip, page, ref, location, timestamp, user_agent)
    else:
        print("🔧 Debug mode ativo — notificações não enviadas.")

    return CheckTracker(
        message="Website Tracker API - No Database Version",
        visitor_ip=visitor_ip,
        user_agent=user_agent,
        timestamp_utc=timestamp,
        location=location,
        status="notification sent (debug)" if debug else "notification sent",
    )
