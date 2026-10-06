"""Quiz service — serves quiz questions."""

import json, os, random

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_quiz: list[dict] = []


def _load():
    global _quiz
    if not _quiz:
        with open(os.path.join(_DATA_DIR, "quiz.json"), encoding="utf-8") as f:
            _quiz = json.load(f)


def get_questions(count: int = 10, category: str | None = None) -> list[dict]:
    _load()
    pool = _quiz
    if category:
        pool = [q for q in _quiz if q.get("category") == category]
    if len(pool) <= count:
        return pool
    return random.sample(pool, count)


def get_all() -> list[dict]:
    _load()
    return _quiz


def handle_chat(user_input: str) -> dict:
    _load()
    q = random.choice(_quiz)
    opts = "\n".join(f"  {chr(65+i)}. {o}" for i, o in enumerate(q["options"]))
    return {
        "response": (
            f"Here's a quiz question for you!\n\n"
            f"**{q['question']}**\n\n{opts}\n\n"
            f"Think about it, then check the Quiz section for more questions!"
        ),
        "type": "quiz",
        "data": q,
    }
