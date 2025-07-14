from fastapi import Header, HTTPException, status, Request
from app.config.settings import settings
from app.logger import logger


async def verify_token(
    token: str = Header(..., alias="X-Tracker-Token"), request: Request = None

):
    masked_key = token[:4] + "****" if token else "None"
    client_ip = request.client.host if request else "unknown"
    """
    Dependency to verify the Tracker API token.
    Raises 403 if invalid.
    """
    if token != settings.TOKEN:
        logger.warning(
            f"Unauthorized access attempt - IP={client_ip}, API_KEY={masked_key}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing token."
        )
    logger.info(f"Authorized access - IP={client_ip}, API_KEY={masked_key}")
