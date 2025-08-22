from datetime import datetime, timezone
from fastapi import Request
from app.services.location_service import get_location


async def collect_request_context(request: Request):
    """
    Returns standard tracking information for a request.
    """
    visitor_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    timestamp = datetime.now(timezone.utc)
    location = await get_location(visitor_ip)
    endpoint = request.url.path
    full_url = str(request.url)
    page = request.query_params.get("page", "Website")
    ref = request.query_params.get("ref")

    return {
        "visitor_ip": visitor_ip,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "location": location,
        "endpoint": endpoint,
        "url": full_url,
        "page": page,
        "ref": ref
    }
