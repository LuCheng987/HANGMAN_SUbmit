def mask_answer(answer: str, guessed: set[str]) -> str:
    """Mask unrevealed letters with underscores (case-insensitive)."""
    gs = {c.lower() for c in guessed}
    return "".join([c if c.lower() in gs else "_" for c in answer])


def is_win(answer: str, guessed: set[str]) -> bool:
    """Check if all letters in the answer have been guessed."""
    return set(c.lower() for c in answer if c.isalpha()).issubset(
        set(g.lower() for g in guessed)
    )


def is_lose(lives: int) -> bool:
    """Check if the player has run out of lives."""
    return lives <= 0


def apply_guess(state: dict, letter: str) -> tuple[dict, bool, bool]:
    """
    Process a single guess.
    Returns: (state, is_valid_attempt, is_correct)
    - is_valid_attempt: True if this is a valid and new attempt (alphabetic, not guessed before)
    - is_correct: True if this new attempt is correct
    Rules:
      * Non-alphabetic or length != 1 → ignored, no life lost
      * Already attempted letters (whether correct or wrong) → ignored, no life lost
      * New incorrect guess → lose 1 life
    """
    letter = (letter or "").strip().lower()
    state.setdefault("guessed", set())     # correctly guessed letters
    state.setdefault("wrong", set())       # incorrectly guessed letters
    state.setdefault("attempted", set())   # all attempted letters

    if not letter.isalpha() or len(letter) != 1:
        return state, False, False

    if letter in state["attempted"]:
        return state, False, (letter in state["guessed"])

    state["attempted"].add(letter)
    if letter in state["answer"].lower():
        state["guessed"].add(letter)
        return state, True, True
    else:
        state["wrong"].add(letter)
        state["lives"] -= 1
        return state, True, False
