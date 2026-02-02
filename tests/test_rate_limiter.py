from fastapi.testclient import TestClient

from app.config.settings import settings
from app.main import app

client = TestClient(app)


def test_tracker_rate_limit_exceeded():
    url = "/api/v1/tracker"

    params = {
        "page": "https://www.victorzarzar.com.br",
    }

    headers = {
        "X-Tracker-Token": settings.TOKEN,
    }

    response = client.get(url, params=params, headers=headers)
    assert response.status_code == 200, (
        f"Expected 200, but returned {response.status_code}: {response.text}"
    )

    response = client.get(url, params=params, headers=headers)
    assert response.status_code == 429, (
        f"Expected 429, but returned {response.status_code}: {response.text}"
    )

    data = response.json()

    assert data["error"] == "Too Many Requests"
    assert isinstance(data.get("retry_after_seconds"), int)

    assert "Retry-After" in response.headers
    assert response.headers["Retry-After"].isdigit()
