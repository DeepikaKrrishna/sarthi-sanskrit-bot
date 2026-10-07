"""
API smoke tests for Sarthi Sanskrit Bot.
Run with: python -m pytest tests/ -v
"""
import pytest
import requests

BASE_URL = "http://localhost:8000"


def test_health_endpoint():
    """Health check should return status ok."""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data
        print(f"Health check passed: {data['message']}")
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend not running - skipping live test")


def test_health_response_structure():
    """Health response should contain required fields."""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        data = response.json()
        required_fields = ["status", "service", "version", "timestamp"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend not running - skipping live test")


def test_chat_endpoint_exists():
    """Chat endpoint should accept POST requests."""
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "namaste"},
            timeout=10
        )
        assert response.status_code in [200, 422], \
            f"Unexpected status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend not running - skipping live test")