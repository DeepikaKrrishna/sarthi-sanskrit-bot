"""Local Ollama integration with a graceful local-tool fallback."""

import json
import os
from typing import Any

import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "30"))

SYSTEM_PROMPT = """You are SĀRTHI, a friendly AI companion for learning Sanskrit. Be concise, helpful, and patient.
Explain Sanskrit in simple English, include transliteration and meaning when useful, and use Devanagari when appropriate.
Respect learner level and language preference. Never invent facts; say clearly when information is uncertain.
Use the supplied local tool results as the source of truth."""


def _local_fallback(message: str, tool_result: dict[str, Any] | None, learner_context: dict[str, Any] | None) -> dict[str, Any]:
    response = tool_result.get("response", "") if tool_result else ""
    if response:
        return {
            "response": response,
            "source": "local-tools",
            "ai_unavailable": True,
            "tool_type": tool_result.get("type"),
        }
    level = (learner_context or {}).get("level", "beginner")
    return {
        "response": (
            "SĀRTHI is ready to help with Sanskrit, but the local AI engine is unavailable. "
            f"Your learning level is {level}. You can use the local Dictionary, Translation, Grammar, "
            "Sentence Analysis, Sandhi, Shloka, Lessons, or Quiz tools for reliable answers."
        ),
        "source": "local-tools",
        "ai_unavailable": True,
        "tool_type": tool_result.get("type") if tool_result else None,
    }


def generate_response(
    message: str,
    tool_result: dict[str, Any] | None = None,
    learner_context: dict[str, Any] | None = None,
    conversation_context: str | None = None,
) -> dict[str, Any]:
    """Generate a response with Ollama, or return a local-tool fallback."""
    try:
        with httpx.Client(timeout=OLLAMA_TIMEOUT) as client:
            response = client.post(
                f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": "\n\n".join(
                        [
                            SYSTEM_PROMPT,
                            f"Learner context: {json.dumps(learner_context or {})}",
                            f"Conversation context:\n{conversation_context or message}",
                            f"User request: {message}",
                            f"Local tool result: {json.dumps(tool_result or {})}",
                        ]
                    ),
                    "stream": False,
                    "options": {"temperature": 0.35},
                },
            )
            response.raise_for_status()
            payload = response.json()
            text = payload.get("response", "").strip()
            if not text:
                raise ValueError("Ollama returned an empty response")
            return {"response": text, "source": "ollama", "ai_unavailable": False}
    except (httpx.HTTPError, ValueError, RuntimeError):
        return _local_fallback(message, tool_result, learner_context)
