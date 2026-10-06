"""Bounded conversation context for SĀRTHI."""

import re
from typing import Any


class ConversationService:
    """Keep a recent, relevant history window without sending unlimited data."""

    def __init__(self, limit: int = 8):
        self.limit = max(1, limit)
        self.messages: list[dict[str, Any]] = []

    def add(self, message: dict[str, Any]) -> None:
        self.messages.append({"role": message.get("role", "user"), "content": str(message.get("content", ""))})
        self.messages = self.messages[-self.limit :]

    def build_context(self, current_message: str) -> str:
        if not self.messages:
            return current_message.strip()

        relevant = self.messages[-self.limit :]
        turns = []
        for message in relevant:
            role = "User" if message.get("role") == "user" else "SĀRTHI"
            turns.append(f"{role}: {message.get('content', '')}")
        turns.append(f"Current user: {current_message.strip()}")
        return "\n".join(turns)

    def recent_turns(self) -> list[dict[str, Any]]:
        return list(self.messages)

    def current_entities(self, message: str) -> list[str]:
        """Extract likely entities for follow-up resolution."""
        entities = re.findall(r"[\u0900-\u097F]+(?:[\u0900-\u097F]*[\u0900-\u097F])?", message)
        return entities[:8]
