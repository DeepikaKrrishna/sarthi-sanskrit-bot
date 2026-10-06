"""Tests for the /api/health endpoint."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_status():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert data["application"] == "SĀRTHI"
    assert "version" in data
