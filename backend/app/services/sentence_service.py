"""Sentence analysis service — word-by-word grammatical breakdown."""

import json, re, os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_dictionary: list[dict] = []

# Pre-built sentence analyses for common sentences
KNOWN_ANALYSES = {
    "रामः वनं गच्छति": [
        {"word": "रामः", "role": "Subject", "part_of_speech": "Noun", "gender": "Masculine", "number": "Singular", "case": "Nominative", "meaning": "Rama"},
        {"word": "वनं", "role": "Object", "part_of_speech": "Noun", "gender": "Neuter", "number": "Singular", "case": "Accusative", "meaning": "forest"},
        {"word": "गच्छति", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "goes", "tense": "Present", "person": "Third"},
    ],
    "बालकः फलं खादति": [
        {"word": "बालकः", "role": "Subject", "part_of_speech": "Noun", "gender": "Masculine", "number": "Singular", "case": "Nominative", "meaning": "boy"},
        {"word": "फलं", "role": "Object", "part_of_speech": "Noun", "gender": "Neuter", "number": "Singular", "case": "Accusative", "meaning": "fruit"},
        {"word": "खादति", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "eats", "tense": "Present", "person": "Third"},
    ],
    "छात्रः पुस्तकं पठति": [
        {"word": "छात्रः", "role": "Subject", "part_of_speech": "Noun", "gender": "Masculine", "number": "Singular", "case": "Nominative", "meaning": "student"},
        {"word": "पुस्तकं", "role": "Object", "part_of_speech": "Noun", "gender": "Neuter", "number": "Singular", "case": "Accusative", "meaning": "book"},
        {"word": "पठति", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "reads", "tense": "Present", "person": "Third"},
    ],
    "सीता पुष्पं पश्यति": [
        {"word": "सीता", "role": "Subject", "part_of_speech": "Noun", "gender": "Feminine", "number": "Singular", "case": "Nominative", "meaning": "Sita"},
        {"word": "पुष्पं", "role": "Object", "part_of_speech": "Noun", "gender": "Neuter", "number": "Singular", "case": "Accusative", "meaning": "flower"},
        {"word": "पश्यति", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "sees", "tense": "Present", "person": "Third"},
    ],
    "अहं गच्छामि": [
        {"word": "अहं", "role": "Subject", "part_of_speech": "Pronoun", "gender": "", "number": "Singular", "case": "Nominative", "meaning": "I"},
        {"word": "गच्छामि", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "go", "tense": "Present", "person": "First"},
    ],
    "गुरुः ज्ञानं ददाति": [
        {"word": "गुरुः", "role": "Subject", "part_of_speech": "Noun", "gender": "Masculine", "number": "Singular", "case": "Nominative", "meaning": "teacher"},
        {"word": "ज्ञानं", "role": "Object", "part_of_speech": "Noun", "gender": "Neuter", "number": "Singular", "case": "Accusative", "meaning": "knowledge"},
        {"word": "ददाति", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "gives", "tense": "Present", "person": "Third"},
    ],
    "अहं छात्रः अस्मि": [
        {"word": "अहं", "role": "Subject", "part_of_speech": "Pronoun", "gender": "", "number": "Singular", "case": "Nominative", "meaning": "I"},
        {"word": "छात्रः", "role": "Complement", "part_of_speech": "Noun", "gender": "Masculine", "number": "Singular", "case": "Nominative", "meaning": "student"},
        {"word": "अस्मि", "role": "Verb", "part_of_speech": "Verb", "gender": "", "number": "Singular", "case": "", "meaning": "am", "tense": "Present", "person": "First"},
    ],
}


def _load_dict():
    global _dictionary
    if not _dictionary:
        with open(os.path.join(_DATA_DIR, "dictionary.json"), encoding="utf-8") as f:
            _dictionary = json.load(f)


def _normalize(s: str) -> str:
    return re.sub(r"[।॥\s]+", " ", s).strip()


def analyze_sentence(text: str) -> list[dict] | None:
    norm = _normalize(text)
    for key, analysis in KNOWN_ANALYSES.items():
        if _normalize(key) == norm:
            return analysis
    return None


def _basic_lookup(text: str) -> list[dict]:
    _load_dict()
    tokens = _normalize(text).split()
    results = []
    for token in tokens:
        found = None
        for entry in _dictionary:
            if entry["word"] == token or entry.get("root", "") == token:
                found = entry
                break
        if found:
            results.append({
                "word": token,
                "role": "—",
                "part_of_speech": found["part_of_speech"],
                "gender": found.get("gender", ""),
                "number": found.get("number", ""),
                "case": found.get("case", ""),
                "meaning": found["meaning"],
            })
        else:
            results.append({"word": token, "role": "—", "part_of_speech": "unknown", "gender": "", "number": "", "case": "", "meaning": "(not in dictionary)"})
    return results


def _extract_sentence(text: str) -> str:
    return re.sub(r"(?i)(analyze|analysis|break\s*down|parse|sentence)\s*:?\s*", "", text).strip()


def handle(user_input: str) -> dict:
    sentence = _extract_sentence(user_input)
    analysis = analyze_sentence(sentence)
    if analysis:
        lines = [f"**Sentence Analysis:** {sentence}\n"]
        for w in analysis:
            parts = [f"**{w['word']}**"]
            parts.append(f"  → Role: {w['role']}")
            parts.append(f"  → {w['part_of_speech']}")
            if w.get("gender"):
                parts.append(f"  → Gender: {w['gender']}")
            if w.get("number"):
                parts.append(f"  → Number: {w['number']}")
            if w.get("case"):
                parts.append(f"  → Case: {w['case']}")
            if w.get("tense"):
                parts.append(f"  → Tense: {w['tense']}")
            if w.get("person"):
                parts.append(f"  → Person: {w['person']}")
            parts.append(f"  → Meaning: {w['meaning']}")
            lines.append("\n".join(parts))
        return {"response": "\n\n".join(lines), "type": "sentence_analysis", "data": analysis}

    # fallback: basic dictionary lookup
    basic = _basic_lookup(sentence)
    if any(w["meaning"] != "(not in dictionary)" for w in basic):
        lines = [f"I don't have a full grammatical analysis for this sentence, but here is what I found for each word:\n"]
        for w in basic:
            lines.append(f"**{w['word']}** → {w['meaning']} ({w['part_of_speech']})")
        lines.append("\n_(Basic lookup from local dictionary)_")
        return {"response": "\n".join(lines), "type": "sentence_analysis", "data": basic}

    return {
        "response": "I couldn't analyze that sentence with my current dataset. Try one of these: 'रामः वनं गच्छति', 'बालकः फलं खादति', or 'अहं गच्छामि'.",
        "type": "sentence_analysis",
        "data": None,
    }
