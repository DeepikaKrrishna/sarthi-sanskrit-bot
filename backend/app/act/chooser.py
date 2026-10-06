"""ACT Chooser — maps an intent to the right SĀRTHI tool."""

from app.act.action import execute
from app.services import chatbot_service

SERVICE_MAP = {
    "CHAT": "AI_KNOWLEDGE",
    "TRANSLATE": "TRANSLATE",
    "WORD_MEANING": "WORD_MEANING",
    "GRAMMAR": "GRAMMAR",
    "SENTENCE_ANALYSIS": "SENTENCE_ANALYSIS",
    "SANDHI": "SANDHI",
    "SHLOKA": "SHLOKA",
    "LEARNING": "LEARNING",
    "QUIZ": "QUIZ",
    "VOICE": "VOICE",
    "HELP": "HELP",
    "AI_KNOWLEDGE": "AI_KNOWLEDGE",
    "UNKNOWN": "UNKNOWN",
}


def choose(intent: str):
    """Return the tool name represented by the detected intent."""
    return SERVICE_MAP.get(intent, "UNKNOWN")


def execute_tool(intent: str, user_input: str):
    return execute(intent, user_input)
