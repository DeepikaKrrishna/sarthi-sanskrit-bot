"""Tests for the translation service."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.translation_service import translate_sentence

def test_known_sentence():
    result = translate_sentence("रामः वनं गच्छति")
    assert result is not None
    assert "forest" in result["english"].lower() or "rama" in result["english"].lower()

def test_basic_sentence():
    result = translate_sentence("अहं गच्छामि")
    assert result is not None
    assert "go" in result["english"].lower()

def test_unknown_sentence():
    result = translate_sentence("this is not in the dataset at all xyz")
    assert result is None

def test_english_to_sanskrit():
    result = translate_sentence("The sun rises")
    assert result is not None
    assert "सूर्यः" in result["sanskrit"]
