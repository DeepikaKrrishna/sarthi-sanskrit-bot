"""Lesson service — serves guided learning content."""

import json, os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_lessons: list[dict] = []


def _load():
    global _lessons
    if not _lessons:
        with open(os.path.join(_DATA_DIR, "lessons.json"), encoding="utf-8") as f:
            _lessons = json.load(f)


def get_all() -> list[dict]:
    _load()
    return _lessons


def get_by_id(lesson_id: int) -> dict | None:
    _load()
    for l in _lessons:
        if l["id"] == lesson_id:
            return l
    return None


def handle(user_input: str) -> dict:
    _load()
    lines = ["Here are the available Sanskrit lessons:\n"]
    for l in _lessons:
        lines.append(f"📚 **Lesson {l['id']}: {l['title']}** ({l['level']})")
    lines.append("\nOpen the Learn section to start any lesson, or ask about a specific topic!")
    return {"response": "\n".join(lines), "type": "learning", "data": [{"id": l["id"], "title": l["title"]} for l in _lessons]}
