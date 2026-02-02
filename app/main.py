import logging

from fastapi import FastAPI

from app.config.limiter import setup_rate_limiter
from app.config.logger import logger
from app.config.settings import settings
from app.middlewares.block_bot_middleware import BlockBotMiddleware
from app.middlewares.cors_middleware import add_cors
from app.middlewares.status_code_middleware import StatusCodeAlertMiddleware
from app.views.health_view import router as health_router
from app.views.tracker_view import router

app = FastAPI(
    title=settings.APP_NAME,
    description="Website visitor tracking API with notifications (no database)",
    version="1.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(BlockBotMiddleware)
app.add_middleware(StatusCodeAlertMiddleware)

logger.info("Logger loaded successfully")
logging.getLogger("slowapi").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

setup_rate_limiter(app, enabled=settings.ENABLE_RATE_LIMITER)

add_cors(app)

# Routes
app.include_router(router)
app.include_router(health_router)
