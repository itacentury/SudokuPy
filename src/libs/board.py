import numpy as np

from typing import Dict, List

from libs.cursor import Cursor
from libs.difficulty import Difficulty

class Board():
    """
    Represents the game board for a Sudoku-like game, managing the grid, cursor position, and game state.

    Attributes:
        cursor (Cursor): The cursor object to navigate through the grid.
        grid (np.ndarray): The current state of the game grid.
        reset_grid (np.ndarray): A copy of the original game grid to reset to the initial state.
        current_key (int): The last key pressed by the user, used for game controls.
        highlighted_number (int): The number currently highlighted by the user.
        time (int): The current time spent on the game.
        difficulty (Difficulty): The difficulty level of the game.

    Methods:
        to_json(self) -> Dict[str, List[List[int]]]
        from_json(self, data: Dict[str, List[List[int]]])
    """
    
    def __init__(self, grid: np.ndarray, difficulty: Difficulty) -> None:
        self.cursor: Cursor = Cursor()
        self.grid: np.ndarray = grid
        self.reset_grid: np.ndarray = grid.copy()
        self.current_key: int = 9
        self.highlighted_number: int = 0
        self.time: int = 0
        self.difficulty: Difficulty = difficulty

    def to_json(self) -> Dict[str, List[List[int]]]:
        """
        Serializes the board's state to a JSON dictionary.
        """

        data: Dict[str, List[List[int]]] = {
            "grid": self.grid.tolist(),
            "reset_grid": self.reset_grid.tolist()
        }
        return data
    
    def from_json(self, data: Dict[str, List[List[int]]]) -> None:
        """
        Loads the board's state from a Dict.
        """

        self.grid: np.ndarray = np.array(data["grid"])
        self.reset_grid: np.ndarray = np.array(data["reset_grid"])

    @property
    def grid(self) -> np.ndarray:
        return self._grid
    
    @grid.setter
    def grid(self, value: np.ndarray) -> None:
        self._grid = value

    @property
    def reset_grid(self) -> np.ndarray:
        return self._grid_copy
    
    @reset_grid.setter
    def reset_grid(self, value: np.ndarray) -> None:
        self._grid_copy = value

    @property
    def current_key(self) -> int:
        """
        Values < 32 are special characters, of which only the 'tab' (9) key is needed.
        32 <= Values and <= 126 are "normal" keyboard keys.
        Values >= 258 and <= 261 are the arrow keys.
        """

        return self._current_key
    
    @current_key.setter
    def current_key(self, value: int) -> None:
        if (value < 32 and value != 9) \
                or (126 < value < 258) \
                or value > 261:
            return
        self._current_key = value

    @property
    def highlighted_number(self) -> int:
        return self._highlighted_number
    
    @highlighted_number.setter
    def highlighted_number(self, value: int) -> None:
        if not (0 <= value <= 9):
            return
        self._highlighted_number = value

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()