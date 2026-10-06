"""Shloka service — serves Sanskrit verses."""

import json, os, random

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_shlokas: list[dict] = []


def _load():
    global _shlokas
    if not _shlokas:
        with open(os.path.join(_DATA_DIR, "shlokas.json"), encoding="utf-8") as f:
            _shlokas = json.load(f)


def get_all() -> list[dict]:
    _load()
    return _shlokas


def get_by_id(shloka_id: int) -> dict | None:
    _load()
    for s in _shlokas:
        if s["id"] == shloka_id:
            return s
    return None


def search(query: str) -> list[dict]:
    _load()
    q = query.lower()
    return [s for s in _shlokas if q in s["sanskrit"] or q in s["transliteration"].lower() or q in s["meaning"].lower() or q in s.get("source", "").lower()]


def handle(user_input: str) -> dict:
    _load()
    # pick a random shloka to share
    shloka = random.choice(_shlokas)
    return {
        "response": (
            f"📜 **{shloka['sanskrit']}**\n\n"
            f"Transliteration: {shloka['transliteration']}\n\n"
            f"Meaning: {shloka['meaning']}\n\n"
            f"{shloka['explanation']}\n\n"
            f"_Source: {shloka['source']}_\n\n"
            f"Explore more shlokas in the Shlokas section!"
        ),
        "type": "shloka",
        "data": shloka,
    }
