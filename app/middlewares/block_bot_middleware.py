
from app.config.settings import settings
from app.services.location_service import get_location
from app.services.notifiy_detection import notify_tracker_detection
from app.services.request_context_service import collect_request_context
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from app.config.logger import logger


# List of User-Agents considered bots
BOT_USER_AGENTS = {
    "googlebot", "bingbot", "slurp", "duckduckbot", "baiduspider",
    "yandexbot", "sogou", "exabot", "facebot", "ia_archiver"
}


# Function to check if the User-Agent belongs to a known bot
def is_known_bot(user_agent: str) -> bool:
    return any(bot in user_agent.lower() for bot in BOT_USER_AGENTS)


# Middleware to block requests from known bots based on User-Agent
class BlockBotMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("User-Agent", "")
        client_ip = request.client.host
        response = await call_next(request)

        if is_known_bot(user_agent):
            logger.warning(
                f"[Middleware] Blocked bot: IP={client_ip}, UA='{user_agent}'")

            if not settings.DEBUG:
                ctx = await collect_request_context(request)
                notify_tracker_detection(
                    visitor_ip=ctx["visitor_ip"],
                    location=ctx["location"],
                    timestamp=ctx["timestamp"],
                    user_agent=ctx["user_agent"],
                    reason=f"Critical status {response.status_code} Blocked known bot detected (middleware)",
                    endpoint=ctx["endpoint"],
                    url=ctx["url"],
                    page=ctx["page"],
                    ref=ctx["ref"]
                )
            else:
                logger.info(
                    "[Middleware] Debug mode active — notification not sent."
                )

                return JSONResponse(
                    status_code=403,
                    content={"detail": "Bots are not allowed."}
                )

        response = await call_next(request)
        return response
