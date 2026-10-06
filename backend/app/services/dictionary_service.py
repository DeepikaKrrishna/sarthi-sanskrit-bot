"""Dictionary service — looks up Sanskrit words."""

import json, re, os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_dictionary: list[dict] = []


def _load():
    global _dictionary
    if not _dictionary:
        with open(os.path.join(_DATA_DIR, "dictionary.json"), encoding="utf-8") as f:
            _dictionary = json.load(f)


def search(word: str) -> dict | None:
    _load()
    word = word.strip()
    # exact match
    for entry in _dictionary:
        if entry["word"] == word or entry["transliteration"].lower() == word.lower() or entry.get("root", "") == word:
            return entry
    # partial
    for entry in _dictionary:
        if word in entry["word"] or word.lower() in entry["transliteration"].lower() or word.lower() in entry["meaning"].lower():
            return entry
    return None


def get_all() -> list[dict]:
    _load()
    return _dictionary


def _extract_word(text: str) -> str:
    """Try to pull the Sanskrit/English word from a natural-language query."""
    # remove common question frames
    cleaned = re.sub(
        r"(?i)(what\s+(?:does|is)\s+|mean(?:s|ing)?\s*(?:of)?\s*|the\s+word\s+|define\s+|look\s*up\s+)",
        "",
        text,
    ).strip().rstrip("?.,!")
    # If the cleaned text has multiple words, try to find a Devanagari token
    tokens = cleaned.split()
    for t in tokens:
        if re.search(r"[\u0900-\u097F]", t):
            return t
    return tokens[0] if tokens else cleaned


def handle(user_input: str) -> dict:
    word = _extract_word(user_input)
    entry = search(word)
    if entry:
        lines = [
            f"**{entry['word']}**",
            f"Transliteration: {entry['transliteration']}",
            f"Meaning: {entry['meaning']}",
            f"Part of speech: {entry['part_of_speech']}",
        ]
        if entry.get("gender"):
            lines.append(f"Gender: {entry['gender']}")
        if entry.get("case"):
            lines.append(f"Case: {entry['case']}")
        if entry.get("number"):
            lines.append(f"Number: {entry['number']}")
        if entry.get("root"):
            lines.append(f"Root: {entry['root']}")
        if entry.get("example"):
            lines.append(f"\nExample: {entry['example']}")
            lines.append(f"({entry.get('example_meaning', '')})")
        return {"response": "\n".join(lines), "type": "word_meaning", "data": entry}
    return {
        "response": f"I couldn't find **{word}** in my current Sanskrit dictionary. Try another word, or browse the dictionary in the Learn section.",
        "type": "word_meaning",
        "data": None,
    }
