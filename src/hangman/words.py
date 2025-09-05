import random

_DICTIONARY = ["apple", "banana", "cat", "dog", "hi", "python", "unit test"]


def load_dictionary() -> list[str]:
    """Return the dictionary of available words/phrases."""
    return _DICTIONARY


def random_entry(level: str) -> str:
    """
    Return a random word or phrase depending on the level.
    - basic: only single words (no spaces)
    - intermediate: may include phrases with spaces
    - fallback: random choice from dictionary
    """
    if level == "basic":
        candidates = [w for w in _DICTIONARY if " " not in w]
        return random.choice(candidates)
    elif level == "intermediate":
        return random.choice(_DICTIONARY)
    else:
        return random.choice(_DICTIONARY)
