"""Take Action — execute the selected SĀRTHI tool."""

from app.services import (
    chatbot_service,
    dictionary_service,
    translation_service,
    grammar_service,
    sentence_service,
    sandhi_service,
    shloka_service,
    quiz_service,
    lesson_service,
)


SERVICE_MAP = {
    "CHAT": chatbot_service.handle,
    "TRANSLATE": translation_service.handle,
    "WORD_MEANING": dictionary_service.handle,
    "GRAMMAR": grammar_service.handle,
    "SENTENCE_ANALYSIS": sentence_service.handle,
    "SANDHI": sandhi_service.handle,
    "SHLOKA": shloka_service.handle,
    "LEARNING": lesson_service.handle,
    "QUIZ": quiz_service.handle_chat,
    "VOICE": chatbot_service.handle,
    "HELP": chatbot_service.handle_help,
    "AI_KNOWLEDGE": chatbot_service.handle,
    "UNKNOWN": chatbot_service.handle_unknown,
}


def execute(intent: str, user_input: str) -> dict:
    handler = SERVICE_MAP.get(intent, chatbot_service.handle_unknown)
    return handler(user_input)
