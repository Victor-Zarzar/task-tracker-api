from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings


# CORS Middleware
def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
