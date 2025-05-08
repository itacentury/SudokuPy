import sys

from game import Game
from libs.difficulty import Difficulty

def main() -> None:
    argv_len: int = len(sys.argv)
    
    if argv_len > 2:
        print("Too many arguments given!")
        print("Only expecting 0 or 1 argument. Try again.")
        sys.exit(-1)

    difficulty_str: str = "medium"
    if argv_len == 2:
        difficulty_str = sys.argv[1].lower()

    difficulty: Difficulty = Difficulty.from_str(difficulty_str)

    game = Game(difficulty)
    game.run()

if __name__ == "__main__":
    main()