import pytest
from fastapi.testclient import TestClient
import os

# Set dummy env vars for tests so the app loads
os.environ["CRON_SECRET_TOKEN"] = "test-token"

from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_trigger_discovery_no_token():
    response = client.post("/api/opportunities/trigger-discovery")
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate CRON credentials"

def test_trigger_discovery_invalid_token():
    response = client.post(
        "/api/opportunities/trigger-discovery",
        headers={"X-Cron-Token": "invalid-token"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate CRON credentials"

def test_trigger_discovery_valid_token():
    response = client.post(
        "/api/opportunities/trigger-discovery",
        headers={"X-Cron-Token": "test-token"}
    )
    assert response.status_code == 202
    assert response.json()["message"] == "Discovery pipeline triggered successfully"
