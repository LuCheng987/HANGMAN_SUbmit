import pytest
from src.hangman import words


def test_random_word_is_from_dictionary():
    w = words.random_entry("basic")
    assert w in words.load_dictionary()   # Basic correctness
