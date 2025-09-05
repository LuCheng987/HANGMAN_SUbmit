import pytest
from src.hangman import game


def test_game_loop_win(monkeypatch):
    """Simulate a full game where the player wins"""
    # fixed word: "hi"
    monkeypatch.setattr("src.hangman.words.random_entry", lambda _: "hi")

    # simulate user inputs: h, i
    inputs = iter(["h", "i"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = game.run_game(level="basic", lives=3)
    assert result == "WIN"


def test_game_loop_lose(monkeypatch):
    """Simulate a full game where the player loses"""
    # fixed word: "hi"
    monkeypatch.setattr("src.hangman.words.random_entry", lambda _: "hi")

    # simulate user inputs: x, y, z (wrong guesses)
    inputs = iter(["x", "y", "z"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = game.run_game(level="basic", lives=3)
    assert result == "LOSE"
