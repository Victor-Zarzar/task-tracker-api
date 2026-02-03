from fastapi.testclient import TestClient

from app.config.settings import settings
from app.main import app

client = TestClient(app)


def test_tracker_rate_limit_exceeded():
    url = "/api/v1/tracker"
    params = {"page": "https://www.victorzarzar.com.br"}
    headers = {"X-Tracker-Token": settings.TOKEN}

    limit = int(settings.RATE_LIMIT_REQUESTS)

    for _ in range(limit):
        r = client.get(url, params=params, headers=headers)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"

    r = client.get(url, params=params, headers=headers)
    assert r.status_code == 429, f"Expected 429, got {r.status_code}: {r.text}"

    data = r.json()
    assert data["error"] == "Too Many Requests"
    assert isinstance(data.get("retry_after_seconds"), int)

    assert "Retry-After" in r.headers
    assert r.headers["Retry-After"].isdigit()
