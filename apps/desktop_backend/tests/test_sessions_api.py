import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import sessions as sessions_api
from app.services.simulation_service import SimulationService


@pytest.fixture
def client(monkeypatch):
    isolated_service = SimulationService()

    monkeypatch.setattr(
        sessions_api,
        "simulation_service",
        isolated_service,
    )

    return TestClient(app)


def test_create_session(client):
    response = client.post("/api/v1/sessions")

    assert response.status_code == 200

    data = response.json()
    assert data["schema_version"] == "1.0.0"
    assert data["status"] == "created"
    assert data["target"] == "LPC1768"
    assert "session_id" in data


def test_get_session(client):
    created = client.post("/api/v1/sessions")
    session_id = created.json()["session_id"]

    response = client.get(f"/api/v1/sessions/{session_id}")

    assert response.status_code == 200
    assert response.json()["session_id"] == session_id


def test_get_missing_session(client):
    response = client.get("/api/v1/sessions/non-existent-session")

    assert response.status_code == 404


def test_list_sessions(client):
    created = client.post("/api/v1/sessions")
    session_id = created.json()["session_id"]

    response = client.get("/api/v1/sessions")

    assert response.status_code == 200
    assert any(
        session["session_id"] == session_id
        for session in response.json()
    )


def test_delete_session(client):
    created = client.post("/api/v1/sessions")
    session_id = created.json()["session_id"]

    response = client.delete(f"/api/v1/sessions/{session_id}")

    assert response.status_code == 204
    assert client.get(f"/api/v1/sessions/{session_id}").status_code == 404


def test_delete_missing_session(client):
    response = client.delete("/api/v1/sessions/non-existent-session")

    assert response.status_code == 404
