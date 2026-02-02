import pytest
from fastapi import HTTPException
from starlette.requests import Request as StarletteRequest

from app.config.settings import settings
from app.services.auth_service import verify_token


def make_request(ip: str = "127.0.0.1"):
    scope = {
        "type": "http",
        "headers": [],
        "client": (ip, 12345),
    }
    return StarletteRequest(scope)


@pytest.mark.asyncio
async def test_verify_token_valid():
    request = make_request()

    result = await verify_token(
        token=settings.TOKEN,
        request=request,
    )

    assert result is None


@pytest.mark.asyncio
async def test_verify_token_invalid():
    request = make_request()

    with pytest.raises(HTTPException) as exc:
        await verify_token(
            token="invalid-token",
            request=request,
        )

    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"


@pytest.mark.asyncio
async def test_verify_token_none():
    request = make_request()

    with pytest.raises(HTTPException):
        await verify_token(
            token=None,
            request=request,
        )
