import json

from typing import Dict, List, Tuple

from libs.difficulty import Difficulty

class HighScoreManager:
    """
    A manager for handling high scores in a game.

    Attributes:
        filename (str): The name of the file where high scores are stored.
        highscores (Dict[str, List[Tuple[str, int, str]]]): A dictionary containing high scores.

    Methods:
        load_highscore(self) -> Dict[str, List[Tuple[str, int, str]]]
        add_highscore(self, name: str, score: int, difficulty: Difficulty) -> None
        save_highscore(self) -> None
    """

    def __init__(self) -> None:
        """
        Initializes the HighScoreManager with default values.
        
        Examples:
            >>> manager = HighScoreManager()
            >>> isinstance(manager, HighScoreManager)
            True
        """

        self.filename: str = "highscores"
        self.highscores: Dict[str, List[Tuple[str, int, str]]] = self.load_highscore()

    def load_highscore(self) -> Dict[str, List[Tuple[str, int, str]]]:
        """
        Loads high scores from the specified file.

        Returns:
            A dictionary with a title and a list of scores.

        Examples:
            >>> manager = HighScoreManager()
            >>> 'scores' in manager.load_highscore()
            True
        """

        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return {"title": "Highscores", "scores": []}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{self.filename}'.")
            return {"title": "Highscores", "scores": []}

    def add_highscore(self, name: str, score: int, difficulty: Difficulty) -> None:
        """
        Adds a new high score to the highscores list.

        Args:
            name (str): The name of the player.
            score (int): The score achieved by the player.
            difficulty (str): The difficulty level of the game.

        Examples:
            >>> manager = HighScoreManager()
            >>> manager.add_highscore("John Doe", 500, "easy")
            >>> "John Doe" in str(manager.highscores["scores"])
            True
        """

        if "scores" not in self.highscores:
            self.highscores["scores"] = []
        
        insert_index: int = len(self.highscores["scores"])
        for i, existing_entry in enumerate(self.highscores["scores"]):
            existing_score: int = existing_entry['score']
            if score < existing_score:
                insert_index = i
                break

        self.highscores["scores"].insert(insert_index, {'name': name, 'score': score, 'difficulty': str(difficulty)})

    def save_highscore(self) -> None:
        """
        Saves the current high scores to the specified file.
        """

        with open(self.filename, 'w') as file:
            json.dump(self.highscores, file)

    @property
    def highscores(self) -> Dict[str, List[Tuple[str, int, str]]]:
        return self._highscores

    @highscores.setter
    def highscores(self, value: Dict[str, List[Tuple[str, int, str]]]) -> None:
        """
        Examples:
            >>> manager = HighscoreManager()
            >>> manager.highscores = {"test", [("one", 1, "1")]}
            >>> manager.highscores
            {"test", [("one", 1, "1")]}
        """

        self._highscores = value
        if "scores" in self._highscores:
            difficulty_order: Dict[str, int] = {"hard": 0, "medium": 1, "easy": 2}
            self._highscores["scores"].sort(key=lambda item: (difficulty_order[item["difficulty"]], item["score"]))

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()