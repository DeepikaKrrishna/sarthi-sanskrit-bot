import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_accepts_context_and_preserves_existing_api():
    response = client.post(
        "/api/chat",
        json={
            "message": "What does रामः mean?",
            "conversation_history": [
                {"role": "user", "content": "Explain Sanskrit words"},
                {"role": "assistant", "content": "I can help with vocabulary."},
            ],
            "learner_context": {"level": "beginner", "language": "en"},
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "WORD_MEANING"
    assert payload["response"]
    assert payload["source"] in {"ollama", "local-tools"}


def test_chat_rejects_empty_message():
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 400
