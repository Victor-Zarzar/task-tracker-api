from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.models.location import Location
from app.services.location_service import get_location


@pytest.mark.asyncio
@patch("app.services.location_service.set_cached_location")
@patch("app.services.location_service.get_cached_location")
@patch("app.services.location_service.httpx.AsyncClient")
async def test_get_location_success(mock_async_client, mock_get_cache, mock_set_cache):
    ip = "1.1.1.1"

    mock_get_cache.return_value = None
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "city": "São Paulo",
        "region": "SP",
        "country": "BR",
        "loc": "-23.5,-46.6",
    }

    client_instance = AsyncMock()
    client_instance.get.return_value = response
    mock_async_client.return_value.__aenter__.return_value = client_instance

    location = await get_location(ip)

    assert isinstance(location, Location)
    assert location.city == "São Paulo"
    assert location.region == "SP"
    assert location.country == "BR"
    assert location.lat == -23.5
    assert location.lon == -46.6

    mock_set_cache.assert_called_once_with(ip, location)
    client_instance.get.assert_awaited_once_with(f"https://ipinfo.io/{ip}/json")
