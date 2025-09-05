from src.hangman import game

if __name__ == "__main__":
    print("Welcome to the Hangman Game!")
    mode = input("Select mode: 1=basic, 2=intermediate: ")
    level = game.select_mode(mode)
    # Run the interactive version with countdown and status display
    result = game.run_game_interactive(level=level, lives=6, timeout=15)
    print("Game over. Result:", result)
