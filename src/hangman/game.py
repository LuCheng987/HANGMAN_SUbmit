from src.hangman import rules, words, io as io_mod

from src.hangman import rules

def apply_guess_with_validation(state: dict, letter: str) -> dict:
    """Wrapper around rules.apply_guess to keep tests compatible."""
    state, _, _ = rules.apply_guess(state, letter)
    return state

def handle_quit(answer: str) -> str:
    """Return the answer when quitting the game."""
    return answer

def select_mode(user_input: str) -> str:
    if user_input.strip() == "1":
        return "basic"
    elif user_input.strip() == "2":
        return "intermediate"
    else:
        print("⚠️ Invalid input, defaulting to BASIC mode.")
        return "basic"


def _render_status(state: dict):
    masked = rules.mask_answer(state["answer"], state["guessed"])
    tried = " ".join(sorted(state.get("attempted", set())))
    wrong = " ".join(sorted(state.get("wrong", set())))
    print(f"\nWord: {masked}")
    print(f"Tried letters: [{tried}]")
    print(f"Wrong letters: [{wrong}]")
    print(f"Lives left: {state['lives']}")


def run_game_interactive(level="basic", lives=6, timeout=15):
    """Interactive game with countdown timer and status display"""
    answer = words.random_entry(level)
    state = {
        "answer": answer,
        "lives": lives,
        "guessed": set(),
        "wrong": set(),
        "attempted": set(),
    }

    print(f"\nMode selected: {level.upper()}  |  Goal: guess the word/phrase")
    _render_status(state)

    while not rules.is_win(answer, state["guessed"]) and not rules.is_lose(
        state["lives"]
    ):
        # 15-second countdown input
        s = io_mod.timed_input("\nEnter a letter or type quit to exit: ", timeout=timeout)

        if s is None or not s.strip():  # timeout/empty input: lose 1 life
            state["lives"] -= 1
            print("⌛ Timeout or empty input, you lose 1 life.")
            _render_status(state)
            continue

        s = s.strip()
        if s.lower() == "quit":
            print(f"You chose to quit. The answer was: {answer}")
            return "QUIT"

        # Apply guess
        before_life = state["lives"]
        state, is_new, is_correct = rules.apply_guess(state, s)

        if not is_new:
            print("ℹ️ Invalid or already tried input, no life lost.")
        else:
            if is_correct:
                print("✅ Correct! Letter(s) revealed.")
            else:
                print(f"❌ Wrong guess, life lost ({before_life} → {state['lives']}).")

        _render_status(state)

    if rules.is_win(answer, state["guessed"]):
        print(f"\n🎉 Congratulations, you win! The answer was: {answer}")
        return "WIN"
    else:
        print(f"\n💥 Game over. You ran out of lives. The answer was: {answer}")
        return "LOSE"


# Minimal version used for unit tests (no countdown/status display)
def run_game(level="basic", lives=6):
    answer = words.random_entry(level)
    state = {
        "answer": answer,
        "lives": lives,
        "guessed": set(),
        "wrong": set(),
        "attempted": set(),
    }
    while not rules.is_win(answer, state["guessed"]) and not rules.is_lose(
        state["lives"]
    ):
        guess = input("Enter a letter or quit: ").strip()
        if guess == "quit":
            return answer
        state, is_new, _ = rules.apply_guess(state, guess)
    return "WIN" if rules.is_win(answer, state["guessed"]) else "LOSE"


