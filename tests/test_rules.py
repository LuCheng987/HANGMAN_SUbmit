import string

import pytest
from src.hangman import rules

def test_correct_letter_revealed():
    masked = rules.mask_answer("apple", {"a"})
    assert masked == "a____"   # TC-01

def test_multiple_same_letters_revealed():
    masked = rules.mask_answer("apple", {"p"})
    assert masked == "app__"   # TC-02

def test_wrong_guess_deducts_life():
    state = {"answer": "apple", "lives": 3, "guessed": set()}
    new_state = rules.apply_guess(state, "z")
    assert new_state["lives"] == 2   # TC-03

def test_repeated_guess_no_penalty():
    state = {"answer": "apple", "lives": 3, "guessed": {"a"}}
    new_state = rules.apply_guess(state, "a")
    assert new_state["lives"] == 3   # TC-05

def test_win_condition():
    assert rules.is_win("hi", {"h", "i"}) is True   # TC-06

def test_lose_condition():
    assert rules.is_lose(0) is True   # TC-07

def test_case_insensitive_input():
    state = {"answer": "hi", "lives": 3, "guessed": set()}
    state = rules.apply_guess(state, "H")
    assert "h" in state["guessed"]   # TC-15

@pytest.mark.parametrize("letter", list(string.ascii_lowercase))
def test_case_insensitive_all_letters(letter):
    """All 26 letters should be case-insensitive"""
    answer = letter
    state = {"answer": answer, "lives": 3, "guessed": set()}

    # uppercase guess
    state, _, _ = rules.apply_guess(state, letter.upper())
    assert letter in state["guessed"]
    assert state["lives"] == 3

    # lowercase guess
    state = {"answer": answer, "lives": 3, "guessed": set()}
    state, _, _ = rules.apply_guess(state, letter.lower())
    assert letter in state["guessed"]
    assert state["lives"] == 3



@pytest.mark.parametrize("answer, valid, invalid, wrong", [
    ("hi", "h", "1", "z"),
    ("apple", "a", "@", "x"),
    ("dog", "d", "!", "q"),
])
def test_mixed_valid_invalid_inputs(answer, valid, invalid, wrong):
    state = {"answer": answer, "lives": 3, "guessed": set()}

    # valid input
    state, _, _ = rules.apply_guess(state, valid)
    assert valid.lower() in state["guessed"]

    # invalid input
    state, _, _ = rules.apply_guess(state, invalid)
    assert state["lives"] == 3  # no life lost

    # wrong input
    state, _, _ = rules.apply_guess(state, wrong)
    assert state["lives"] == 2  # one life lost
