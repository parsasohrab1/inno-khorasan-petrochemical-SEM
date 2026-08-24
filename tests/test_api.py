import os

os.environ.setdefault("SEMS_MODEL_PATH", "models/__nonexistent_for_tests__.zip")

from fastapi.testclient import TestClient  # noqa: E402

from sems.api.main import app  # noqa: E402
from sems.api.security import DEMO_USERNAME  # noqa: E402

client = TestClient(app)


def _get_token() -> str:
    response = client.post(
        "/auth/token", data={"username": DEMO_USERNAME, "password": "changeme"}
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_status"] == "fallback_baseline_no_trained_model"


def test_login_rejects_bad_credentials():
    response = client.post("/auth/token", data={"username": DEMO_USERNAME, "password": "wrong"})
    assert response.status_code == 401


def test_recommend_requires_auth():
    response = client.post("/recommend", json={})
    assert response.status_code == 401


def test_recommend_returns_action_and_alerts():
    token = _get_token()
    response = client.post(
        "/recommend",
        json={"feed_flow": 100000, "coking_factor": 0.05},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert "recommended_action" in body
    assert "S_C_ratio" in body["recommended_action"]
    assert isinstance(body["alerts"], list)


def test_forecast_energy_endpoint():
    token = _get_token()
    response = client.get(
        "/forecast/energy?horizon_steps=4", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["horizon_steps"] == 4
    assert len(body["predicted_energy_GJ_per_step"]) == 4
