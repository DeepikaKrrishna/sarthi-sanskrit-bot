import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.conversation_service import ConversationService


def test_follow_up_uses_relevant_previous_topic():
    service = ConversationService(limit=6)
    service.add({"role": "user", "content": "Explain रामः"})
    service.add({"role": "assistant", "content": "रामः means Rama"})
    service.add({"role": "user", "content": "Give me its grammatical form"})

    context = service.build_context("Give me its grammatical form")
    assert "रामः" in context
    assert "its grammatical form" in context


def test_context_is_bounded():
    service = ConversationService(limit=3)
    for index in range(5):
        service.add({"role": "user", "content": f"question {index}"})

    context = service.build_context("latest")
    assert "question 0" not in context
    assert "question 4" in context
