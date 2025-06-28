from fastapi import FastAPI
from app.middlewares.cors_middleware import add_cors
from app.services.rate_limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.handlers.exceptions import rate_limit_exceeded_handler
from app.config.settings import settings
from app.views.tracker_view import router

app = FastAPI(
    title=settings.APP_NAME,
    description="Website visitor tracking API with notifications (no database)",
    version="1.0.0",
    debug=settings.DEBUG
)

# Rate Limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS Middleware
add_cors(app)

# Routes
app.include_router(router)
