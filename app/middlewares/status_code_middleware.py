from starlette.middleware.base import BaseHTTPMiddleware
from app.services.notifiy_detection import notify_tracker_detection
from app.config.logger import logger
from app.config.settings import settings
from app.services.request_context_service import collect_request_context


class StatusCodeAlertMiddleware(BaseHTTPMiddleware):
    CRITICAL_CODES = {401, 403, 429, 503}

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if response.status_code in self.CRITICAL_CODES:
            logger.warning(
                f"[Middleware] Critical status {response.status_code} to {request.client.host}")

            if not settings.DEBUG:
                ctx = await collect_request_context(request)
                notify_tracker_detection(
                    visitor_ip=ctx["visitor_ip"],
                    location=ctx["location"],
                    timestamp=ctx["timestamp"],
                    user_agent=ctx["user_agent"],
                    reason=f"Critical status {response.status_code} detected (middleware)",
                    endpoint=ctx["endpoint"],
                    url=ctx["url"],
                    page=ctx["page"],
                    ref=ctx["ref"]
                )
            else:
                logger.info(
                    "[Middleware] Debug mode active — notification not sent."
                )

        return response
