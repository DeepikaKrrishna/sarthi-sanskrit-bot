"""Tests for the dictionary service."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.dictionary_service import search

def test_known_word_devanagari():
    entry = search("रामः")
    assert entry is not None
    assert entry["meaning"] == "Rama (a proper name, an avatar of Vishnu)"

def test_known_word_transliteration():
    entry = search("gacchati")
    assert entry is not None
    assert "goes" in entry["meaning"].lower()

def test_unknown_word():
    entry = search("xyznonexistent")
    assert entry is None

def test_verb_lookup():
    entry = search("पठति")
    assert entry is not None
    assert entry["part_of_speech"] == "verb"

def test_pronoun_lookup():
    entry = search("अहम्")
    assert entry is not None
    assert entry["part_of_speech"] == "pronoun"
