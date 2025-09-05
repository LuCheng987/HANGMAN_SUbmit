import pytest
from src.hangman import game


def test_invalid_input_ignored():
    state = {"answer": "apple", "lives": 3, "guessed": set()}
    new_state = game.apply_guess_with_validation(state, "3")
    assert new_state["lives"] == 3   # TC-08


def test_mode_selection_basic():
    assert game.select_mode("1") == "basic"   # TC-09


def test_mode_selection_intermediate():
    assert game.select_mode("2") == "intermediate"   # TC-10


def test_mode_selection_invalid_defaults_to_basic(capsys):
    mode = game.select_mode("xyz")
    out, _ = capsys.readouterr()
    assert "Invalid" in out
    assert mode == "basic"   # TC-11


def test_quit_game_returns_answer(mocker):
    mocker.patch("builtins.input", return_value="quit")
    result = game.handle_quit("hello")
    assert result == "hello"   # TC-13


def test_performance_many_inputs():
    state = {"answer": "apple", "lives": 10, "guessed": set()}
    for _ in range(1000):  # rapid inputs
        state = game.apply_guess_with_validation(state, "z")
    assert state["lives"] <= 10   # program should not hang, must complete   # TC-14


def test_performance_many_inputs():
    """Simulate many rapid inputs to ensure program does not hang"""
    state = {"answer": "apple", "lives": 10, "guessed": set()}

    for _ in range(1000):  # simulate 1000 rapid guesses
        state = game.apply_guess_with_validation(state, "z")

    # Program must complete and lives should not exceed initial value
    assert state["lives"] <= 10