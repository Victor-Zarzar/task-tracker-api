from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from app.logger import logger


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

        if is_known_bot(user_agent):
            logger.warning(
                f"[Middleware] Blocked bot: IP={client_ip}, UA='{user_agent}'")
            return JSONResponse(
                status_code=403,
                content={"detail": "Bots are not allowed."}
            )

        response = await call_next(request)
        return response
