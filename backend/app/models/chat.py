"""Chat API models."""

from typing import Any

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(pattern=r"^(user|assistant)$")
    content: str = Field(min_length=1, max_length=20000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    conversation_history: list[ChatMessage] = Field(default_factory=list, max_length=20)
    learner_context: dict[str, Any] = Field(default_factory=dict)
