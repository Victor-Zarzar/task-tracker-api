from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tracker_rate_limit_exceeded():
    url = "/api/v1/tracker"
    params = {"page": "Homepage"}

    response = client.get(url, params=params)
    assert response.status_code == 200, (
        f"Esperado 200, mas retornou {response.status_code}: {response.text}"
    )

    response = client.get(url, params=params)
    assert response.status_code == 429, (
        f"Esperado 429, mas retornou {response.status_code}: {response.text}"
    )

    data = response.json()
    assert data.get("error") == "Too Many Requests", f"Erro inesperado: {data}"
    assert "limite de 1 per 1 minute" in data.get("message", ""), (
        f"Mensagem inesperada: {data}"
    )
    assert isinstance(data.get("retry_after_seconds"), int), (
        "Campo `retry_after_seconds` ausente ou inválido"
    )
