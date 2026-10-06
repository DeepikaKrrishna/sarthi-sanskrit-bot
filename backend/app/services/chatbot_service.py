"""General chat, help, and unknown-intent handler."""

import random

CHAT_RESPONSES = {
    "hello": "Namaste! 🙏 Welcome to SĀRTHI. I am your Sanskrit learning assistant. How can I help you today?",
    "hi": "Namaste! 🙏 I am SĀRTHI, your Sanskrit learning companion. Ask me about words, grammar, translations, shlokas, or start a lesson!",
    "namaste": "नमस्ते! 🙏 Welcome! I can help you learn Sanskrit — try asking me a word meaning, a translation, or explore grammar.",
    "thanks": "You are welcome! In Sanskrit, we say 'धन्यवादः' (dhanyavādaḥ). Keep learning! 📚",
    "thank you": "धन्यवादः! Happy to help. Feel free to ask anything about Sanskrit.",
    "bye": "Until next time! In Sanskrit: पुनर्मिलामः (punar milāmaḥ) — we shall meet again! 🙏",
    "what is sanskrit": "Sanskrit (संस्कृतम्) is one of the oldest languages in the world, meaning 'refined' or 'perfected'. It is the classical language of India with a rich literary tradition spanning thousands of years. It has a highly systematic grammar described by the ancient grammarian Pāṇini. Would you like to start a lesson or explore some words?",
    "who are you": "I am SĀRTHI (Sanskrit AI Research & Teaching Helper Interface) — your local-first Sanskrit learning assistant. I can help you with word meanings, translations, grammar, shlokas, quizzes, and guided lessons. All processing happens locally with no external API calls.",
}

FALLBACK_RESPONSES = [
    "That's an interesting question! While I focus on Sanskrit learning, I can help you with word meanings, translations, grammar explanations, shlokas, and quizzes. What would you like to explore?",
    "I'm best at helping with Sanskrit! Try asking me about a word meaning, request a translation, or explore the grammar section.",
    "I'd love to help with that! My expertise is in Sanskrit — try typing a Sanskrit word, asking for a translation, or starting a quiz.",
]


def handle(user_input: str) -> dict:
    text = user_input.lower().strip()
    for key, response in CHAT_RESPONSES.items():
        if key in text:
            return {"response": response, "type": "chat"}
    return {"response": random.choice(FALLBACK_RESPONSES), "type": "chat"}


def handle_help(user_input: str) -> dict:
    return {
        "response": (
            "Here is what I can do:\n\n"
            "📖 **Word Meaning** — Type any Sanskrit word to get its meaning, transliteration, and grammar info.\n\n"
            "🔄 **Translation** — Translate between Sanskrit and English. Try: 'Translate रामः वनं गच्छति'\n\n"
            "📝 **Grammar** — Ask about nouns, verbs, cases, tenses, and sentence structure.\n\n"
            "🔍 **Sentence Analysis** — Enter a Sanskrit sentence to get a word-by-word breakdown.\n\n"
            "🔗 **Sandhi** — Learn about how Sanskrit sounds join together.\n\n"
            "📜 **Shlokas** — Explore famous Sanskrit verses with meanings and explanations.\n\n"
            "📚 **Lessons** — Start guided lessons from basic vocabulary to sentence construction.\n\n"
            "🧪 **Quiz** — Test your Sanskrit knowledge with interactive quizzes.\n\n"
            "🎤 **Voice** — Use the Voice Studio for speech-to-text and text-to-speech (browser-dependent).\n\n"
            "Try typing a Sanskrit word like **रामः** or ask me to **translate** something!"
        ),
        "type": "help",
    }


def handle_unknown(user_input: str) -> dict:
    return {
        "response": (
            "I'm not sure I understood that. I'm SĀRTHI, your Sanskrit learning assistant.\n\n"
            "Here are some things you can try:\n"
            "• Type a Sanskrit word like **धर्मः** to get its meaning\n"
            "• Say **'translate अहं गच्छामि'** for a translation\n"
            "• Ask about **grammar**, **sandhi**, or **shlokas**\n"
            "• Type **'help'** to see everything I can do"
        ),
        "type": "unknown",
    }
