"""ACT Analyzer — determines user intent, language, entities, and learner needs."""

import re

INTENT_PATTERNS = {
    "TRANSLATE": [
        r"\btranslat",
        r"\bmean(?:s|ing)?\s+(?:of|in)\b",
        r"\bin\s+(?:english|sanskrit)\b",
        r"\bhow\s+(?:do\s+you\s+)?say\b",
        r"\bconvert\b",
    ],
    "WORD_MEANING": [
        r"\bwhat\s+(?:does|is)\s+\S+\s+mean",
        r"\bmeaning\s+of\b",
        r"\bdefin(?:e|ition)\b",
        r"\blook\s*up\b",
    ],
    "GRAMMAR": [
        r"\bgrammar\b",
        r"\bconjugat",
        r"\bdeclen",
        r"\bverb\s+form",
        r"\bcase(?:s)?\b",
        r"\bविभक्ति",
        r"\btense",
        r"\bgender\b",
        r"\bnoun\b",
        r"\bpronoun\b",
    ],
    "SENTENCE_ANALYSIS": [
        r"\banalyze?\b",
        r"\banalysis\b",
        r"\bbreak\s*down\b",
        r"\bparse\b",
        r"\bsentence\s+structure\b",
    ],
    "SANDHI": [
        r"\bsandhi\b",
        r"\bसन्धि\b",
        r"\bjoin(?:ing)?\s+(?:of\s+)?(?:words|sounds)\b",
        r"\bsplit\b.*\bword",
    ],
    "SHLOKA": [
        r"\bshloka\b",
        r"\bश्लोक\b",
        r"\bverse\b",
        r"\bmantra\b",
        r"\bsukt",
        r"\bprayer\b",
    ],
    "LEARNING": [
        r"\bteach\b",
        r"\blearn\b",
        r"\blesson\b",
        r"\btutorial\b",
        r"\bbegin(?:ner)?\b",
        r"\bintroduc",
        r"\bbasic\b",
    ],
    "QUIZ": [
        r"\bquiz\b",
        r"\btest\s+(?:me|my)\b",
        r"\bpractice\b",
        r"\bexercise\b",
    ],
    "VOICE": [
        r"\bspeak\b",
        r"\bpronounce\b",
        r"\bpronunciation\b",
        r"\blisten\b",
        r"\bsay\s+(?:it|this|that)\b",
        r"\bread\s+(?:it\s+)?aloud\b",
    ],
    "HELP": [
        r"\bhelp\b",
        r"\bwhat\s+can\s+you\s+do\b",
        r"\bfeature",
        r"\bhow\s+(?:does\s+)?(?:this|it)\s+work",
        r"\bcommand",
    ],
}

SANSKRIT_PATTERN = re.compile(r"[\u0900-\u097F]")
ENGLISH_PATTERN = re.compile(r"[a-zA-Z]{2,}")


def analyze(text: str, previous_context: str | None = None, learner_context: dict | None = None) -> dict:
    """Analyze intent, language, entities, topic, difficulty, and context needs."""
    text = text.strip()
    text_lower = text.lower()
    if not text:
        return {"intent": "UNKNOWN", "confidence": 0.0, "details": "empty input", "language": "unknown", "entities": [], "topic": None, "difficulty": "beginner", "requires_tool": False, "can_answer_with_ai": True}

    scores: dict[str, float] = {}
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                scores[intent] = scores.get(intent, 0) + 1.0

    has_sanskrit = bool(SANSKRIT_PATTERN.search(text))
    has_english_words = bool(ENGLISH_PATTERN.search(text))
    if has_sanskrit and not has_english_words:
        words = text.split()
        if len(words) == 1:
            scores["WORD_MEANING"] = scores.get("WORD_MEANING", 0) + 2.0
        else:
            scores["TRANSLATE"] = scores.get("TRANSLATE", 0) + 2.0

    if not scores:
        scores["CHAT"] = 1.0
        if previous_context and re.search(r"\b(?:it|this|that|them|these|those|example|more simply)\b", text_lower):
            scores["AI_KNOWLEDGE"] = 1.5

    best_intent = max(scores, key=scores.get)
    confidence = min(scores[best_intent] / 3.0, 1.0)
    entity_matches = re.findall(r"[\u0900-\u097F]+", text)
    entities = list(dict.fromkeys(entity_matches))
    level = (learner_context or {}).get("level", "beginner")
    if level not in {"beginner", "intermediate", "advanced"}:
        level = "beginner"

    return {
        "intent": best_intent,
        "confidence": round(confidence, 2),
        "details": f"matched {best_intent}",
        "language": "sanskrit" if has_sanskrit else "english" if has_english_words else "mixed",
        "entities": entities,
        "topic": text[:160],
        "difficulty": level,
        "requires_tool": best_intent not in {"CHAT", "AI_KNOWLEDGE", "HELP", "UNKNOWN"},
        "can_answer_with_ai": best_intent in {"CHAT", "AI_KNOWLEDGE", "HELP"},
    }
