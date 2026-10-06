"""Sandhi service — explains sandhi rules and examples."""

import json, os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_sandhi: dict = {}


def _load():
    global _sandhi
    if not _sandhi:
        with open(os.path.join(_DATA_DIR, "sandhi.json"), encoding="utf-8") as f:
            _sandhi = json.load(f)


def get_all() -> dict:
    _load()
    return _sandhi


def find_example(word: str) -> dict | None:
    _load()
    word = word.strip()
    for ex in _sandhi.get("examples", []):
        if ex["combined"] == word or word in ex.get("parts", []):
            return ex
    return None


def handle(user_input: str) -> dict:
    _load()
    text = user_input.strip()

    # Check if they are asking about a specific word
    import re
    sanskrit_tokens = re.findall(r"[\u0900-\u097F]+", text)
    for token in sanskrit_tokens:
        ex = find_example(token)
        if ex:
            return {
                "response": (
                    f"**Sandhi Analysis: {ex['combined']}**\n\n"
                    f"Parts: {' + '.join(ex['parts'])}\n"
                    f"Type: {ex['type'].title()} Sandhi\n"
                    f"Meaning: {ex['meaning']}\n"
                    f"Breakdown: {ex['breakdown']}"
                ),
                "type": "sandhi",
                "data": ex,
            }

    # General sandhi explanation
    lines = [f"## Sandhi (सन्धि)\n", _sandhi["explanation"], ""]
    for stype in _sandhi.get("types", []):
        lines.append(f"### {stype['name']}")
        lines.append(stype["description"])
        for rule in stype.get("rules", [])[:2]:
            lines.append(f"  • {rule['rule']}  →  {rule.get('result', '')} ({rule.get('meaning', '')})")
        lines.append("")
    lines.append("Try asking about a specific word like **देवालयः** or **सूर्योदयः** for a detailed breakdown.")
    return {"response": "\n".join(lines), "type": "sandhi", "data": _sandhi}
