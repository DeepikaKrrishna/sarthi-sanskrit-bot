"""Grammar service — returns grammar topics and explanations."""

import json, re, os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_grammar: dict = {}


def _load():
    global _grammar
    if not _grammar:
        with open(os.path.join(_DATA_DIR, "grammar.json"), encoding="utf-8") as f:
            _grammar = json.load(f)


def get_all_topics() -> list[dict]:
    _load()
    return _grammar.get("topics", [])


def get_topic(topic_id: str) -> dict | None:
    _load()
    for t in _grammar.get("topics", []):
        if t["id"] == topic_id:
            return t
    return None


def find_topic(query: str) -> dict | None:
    _load()
    q = query.lower()
    for t in _grammar.get("topics", []):
        if t["id"] in q or t["title"].lower() in q:
            return t
    # partial keyword match
    for t in _grammar.get("topics", []):
        if any(kw in q for kw in [t["id"], t["title"].lower().split("(")[0].strip()]):
            return t
    return None


def handle(user_input: str) -> dict:
    _load()
    topic = find_topic(user_input)
    if topic:
        lines = [f"## {topic['title']}\n", topic["explanation"], ""]
        for ex in topic.get("examples", []):
            lines.append(f"**{ex['sanskrit']}** — {ex['english']}")
            if ex.get("note"):
                lines.append(f"  _{ex['note']}_")
        if topic.get("practice"):
            p = topic["practice"]
            lines.append(f"\n**Practice:** {p['question']}")
            for opt in p.get("options", []):
                lines.append(f"  • {opt}")
        return {"response": "\n".join(lines), "type": "grammar", "data": topic}

    # general overview
    topics = get_all_topics()
    lines = ["Here are the grammar topics I can explain:\n"]
    for t in topics:
        lines.append(f"• **{t['title']}**")
    lines.append("\nAsk about any topic — for example, 'Explain Sanskrit nouns' or 'Tell me about verb tenses'.")
    return {"response": "\n".join(lines), "type": "grammar", "data": {"available_topics": [t["id"] for t in topics]}}
