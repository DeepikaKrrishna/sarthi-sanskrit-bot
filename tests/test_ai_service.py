import os
import sys
from unittest.mock import patch

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.app.services.ai_service import generate_response


def test_ai_service_returns_friendly_error_when_ollama_unavailable():
    with patch("backend.app.services.ai_service.httpx.Client") as client_factory:
        client_factory.side_effect = RuntimeError("connection refused")
        result = generate_response(
            "What is Sandhi?",
            tool_result={"type": "sandhi", "response": "Sandhi joins words"},
            learner_context={"level": "beginner"},
        )

    assert result["source"] == "local-tools"
    assert "Sandhi joins words" in result["response"]
    assert result["ai_unavailable"] is True
