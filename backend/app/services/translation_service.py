"""Translation service — Sanskrit ↔ English using local dataset."""

import json, re, os
from app.services.dictionary_service import search as dict_search, _load as dict_load, _dictionary

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_translations: list[dict] = []

SANSKRIT_RE = re.compile(r"[\u0900-\u097F]")


def _load():
    global _translations
    if not _translations:
        with open(os.path.join(_DATA_DIR, "translations.json"), encoding="utf-8") as f:
            _translations = json.load(f)


def _normalize(s: str) -> str:
    return re.sub(r"[।॥\s]+", " ", s).strip().rstrip(".!?,।")


def translate_sentence(text: str) -> dict | None:
    _load()
    norm = _normalize(text)
    is_sanskrit = bool(SANSKRIT_RE.search(text))

    for t in _translations:
        if is_sanskrit:
            if _normalize(t["sanskrit"]) == norm:
                return t
        else:
            if t["english"].lower().strip(".") == norm.lower():
                return t

    # partial match
    for t in _translations:
        if is_sanskrit:
            if norm in _normalize(t["sanskrit"]) or _normalize(t["sanskrit"]) in norm:
                return t
        else:
            if norm.lower() in t["english"].lower():
                return t
    return None


def word_by_word(text: str) -> list[dict]:
    """Fall back to word-by-word translation using the dictionary."""
    dict_load()
    tokens = re.split(r"\s+", _normalize(text))
    results = []
    for token in tokens:
        entry = dict_search(token)
        if entry:
            results.append({"word": token, "meaning": entry["meaning"], "info": entry["part_of_speech"]})
        else:
            results.append({"word": token, "meaning": "(not found)", "info": ""})
    return results


def _extract_sentence(text: str) -> str:
    cleaned = re.sub(r"(?i)(translate|translation|convert|in\s+english|in\s+sanskrit|to\s+english|to\s+sanskrit)\s*:?\s*", "", text).strip()
    return cleaned


def handle(user_input: str) -> dict:
    sentence = _extract_sentence(user_input)
    match = translate_sentence(sentence)
    if match:
        is_sanskrit = bool(SANSKRIT_RE.search(sentence))
        if is_sanskrit:
            return {
                "response": (
                    f"**Sanskrit:** {match['sanskrit']}\n"
                    f"**Transliteration:** {match['transliteration']}\n"
                    f"**English:** {match['english']}\n\n"
                    f"_(Translation from local dataset)_"
                ),
                "type": "translation",
                "data": match,
            }
        else:
            return {
                "response": (
                    f"**English:** {match['english']}\n"
                    f"**Sanskrit:** {match['sanskrit']}\n"
                    f"**Transliteration:** {match['transliteration']}\n\n"
                    f"_(Translation from local dataset)_"
                ),
                "type": "translation",
                "data": match,
            }

    # word-by-word fallback
    wbw = word_by_word(sentence)
    if any(w["meaning"] != "(not found)" for w in wbw):
        lines = ["I don't have an exact sentence translation, but here is a word-by-word breakdown:\n"]
        for w in wbw:
            tag = f" ({w['info']})" if w["info"] else ""
            lines.append(f"**{w['word']}** → {w['meaning']}{tag}")
        lines.append("\n_(Word-by-word from local dictionary)_")
        return {"response": "\n".join(lines), "type": "translation", "data": wbw}

    return {
        "response": f"I couldn't translate that sentence from my local dataset. Try a simpler sentence, or look up individual words.",
        "type": "translation",
        "data": None,
    }
