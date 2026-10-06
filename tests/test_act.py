"""Tests for the ACT analyzer intent detection."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.act.analyzer import analyze

def test_word_meaning_intent():
    result = analyze("What does रामः mean?")
    assert result["intent"] == "WORD_MEANING"

def test_translate_intent():
    result = analyze("Translate अहं छात्रः अस्मि")
    assert result["intent"] == "TRANSLATE"

def test_grammar_intent():
    result = analyze("Explain Sanskrit grammar")
    assert result["intent"] == "GRAMMAR"

def test_sandhi_intent():
    result = analyze("What is Sandhi?")
    assert result["intent"] == "SANDHI"

def test_quiz_intent():
    result = analyze("Give me a quiz")
    assert result["intent"] == "QUIZ"

def test_shloka_intent():
    result = analyze("Show me a shloka")
    assert result["intent"] == "SHLOKA"

def test_learn_intent():
    result = analyze("Teach me Sanskrit")
    assert result["intent"] == "LEARNING"

def test_help_intent():
    result = analyze("What can you do?")
    assert result["intent"] == "HELP"

def test_pure_sanskrit_word():
    result = analyze("धर्मः")
    assert result["intent"] == "WORD_MEANING"

def test_pure_sanskrit_sentence():
    result = analyze("रामः वनं गच्छति")
    assert result["intent"] == "TRANSLATE"

def test_empty_input():
    result = analyze("")
    assert result["intent"] == "UNKNOWN"

def test_general_chat():
    result = analyze("hello")
    assert result["intent"] == "CHAT"
