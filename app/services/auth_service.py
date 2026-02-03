from fastapi import Header, HTTPException, Request

from app.config.logger import logger
from app.config.settings import settings


async def verify_token(
    token: str = Header(..., alias="X-Tracker-Token"), request: Request = None
):
    masked_key = token[:4] + "****" if token else "None"
    client_ip = request.client.host if request else "unknown"
    if token != settings.TOKEN:
        logger.warning(
            f"Unauthorized access attempt - IP={client_ip}, API_KEY={masked_key}"
        )
        raise HTTPException(status_code=401, detail="Unauthorized")

    logger.info(f"Authorized access - IP={client_ip}, API_KEY={masked_key}")
