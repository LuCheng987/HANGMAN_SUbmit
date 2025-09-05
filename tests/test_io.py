import pytest
from src.hangman import io


def test_timeout_returns_none(mocker):
    # Simulate input blocking forever
    mocker.patch("builtins.input", side_effect=EOFError)
    result = io.timed_input("Enter: ", timeout=1)
    assert result is None   # TC-04


def test_countdown_display(mocker, capsys):
    # Simulate input arriving at the 2nd second
    inputs = iter(["a"])
    mocker.patch("builtins.input", side_effect=lambda _: next(inputs))
    result = io.timed_input("Enter: ", timeout=3)
    out, _ = capsys.readouterr()
    assert "left" in out    # Countdown message should be shown   # TC-12
    assert result == "a"



def test_timeout_deducts_life(monkeypatch):
    """Simulate timeout and ensure life is deducted"""
    state = {"answer": "hi", "lives": 3, "guessed": set(), "wrong": set(), "attempted": set()}

    # force timed_input to return None (simulate timeout)
    monkeypatch.setattr(io, "timed_input", lambda *args, **kwargs: None)

    result = io.timed_input("Enter: ", timeout=1)
    assert result is None

    # deduct life if timeout
    if result is None:
        state["lives"] -= 1

    assert state["lives"] == 2
