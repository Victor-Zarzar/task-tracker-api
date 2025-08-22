from app.services.cache_service import get_cached_location, set_cached_location
import httpx
from app.models.tracker_model import Location
from app.config.logger import logger


async def get_location(ip: str) -> Location:

    cached = get_cached_location(ip)
    if cached:
        logger.debug(f"Cache hit for IP: {ip}")
        return cached

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"https://ipinfo.io/{ip}/json")

            if resp.status_code == 200:
                data = resp.json()
                lat, lon = None, None

                if "loc" in data:
                    try:
                        lat_str, lon_str = data["loc"].split(",")
                        lat, lon = float(lat_str), float(lon_str)
                    except ValueError:
                        logger.warning(
                            f"Failed to parse coordinates to IP {ip}")

                location = Location(
                    city=data.get("city"),

                    region=data.get("region"),
                    country=data.get("country"),

                    lat=lat,
                    lon=lon,
                    loc=data.get("loc"),
                )

                set_cached_location(ip, location)
                return location

            logger.warning(
                f"Failed to query location - Status {resp.status_code}")

    except Exception as e:

        logger.error(f"Location query error - IP: {ip} | Erro: {e}")
        logger.debug("Full stacktrace:", exc_info=True)

    return Location()
