"""Test suite for ML inference service."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "version" in data
    assert "uptime_seconds" in data

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "inference_requests_total" in response.text

def test_predict_success():
    payload = {
        "inputs": [
            {"id": "row_1", "features": [1.2, 0.4, -0.5, 2.1]},
            {"id": "row_2", "features": [-1.0, -2.0, 0.1, -0.4]}
        ],
        "model_version": "1.0.0"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 2
    assert data["predictions"][0]["id"] == "row_1"
    assert "latency_ms" in data
    assert data["latency_ms"] >= 0

def test_predict_validation_error():
    # Missing features field
    payload = {
        "inputs": [
            {"id": "bad_row"}
        ]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
