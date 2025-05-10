import random
import numpy as np

from typing import List, Optional, Dict, Tuple

from libs.checker import SudokuChecker
from libs.solver import SudokuSolver
from libs.difficulty import Difficulty

class SudokuGenerator:
    """
    A class to generate Sudoku puzzles of a specified difficulty.

    Attributes:
        size (int): The size of the Sudoku board (e.g., 9 for a standard Sudoku).
        board (np.ndarray): The current state of the Sudoku board.
        rng (np.random.Generator): A random number generator instance.
        subgrid_size (int): The size of the subgrids in the Sudoku board.
        difficulty (Difficulty): The difficulty level of the Sudoku puzzle.

    Methods:
        generate(self) -> Optional[np.ndarray]
        __fill_board(self, row: int = 0, col: int = 0) -> bool
        __is_safe(self, row: int, col: int, num: int) -> bool
        __valid_sudoku(self) -> bool
        __remove_cells(self) -> None
        __has_unique_solution(self) -> bool
    """

    def __init__(self, difficulty: Difficulty, size: int = 9) -> None:
        """
        Initializes the SudokuGenerator with a given difficulty and board size.

        Args:
            difficulty (Difficulty): The difficulty level for the generated Sudoku puzzle.
            size (int, optional): The size of the Sudoku board. Defaults to 9.
        """

        self.size: int = size
        self.board: np.ndarray = np.zeros((self.size, self.size), dtype=int)
        self.rng: np.random.Generator = np.random.default_rng(seed=random.randint(1, 10 ** 10))
        self.subgrid_size: int = int(np.sqrt(self.size))
        self.difficulty: Difficulty = difficulty
        
    def generate(self) -> Optional[np.ndarray]:
        """
        Generates a Sudoku puzzle and returns the board.

        Returns:
            Optional[np.ndarray]: The generated Sudoku board or None if generation fails.
        """

        self.__fill_board()
        if self.__valid_sudoku():
            self.__remove_cells()
            return self.board

        return None

    def __fill_board(self, row: int = 0, col: int = 0) -> bool:
        """
        Recursively fills the Sudoku board with valid numbers.

        Args:
            row (int, optional): The current row to fill. Defaults to 0.
            col (int, optional): The current column to fill. Defaults to 0.

        Returns:
            bool: True if the board was successfully filled, False otherwise.
        """

        if row == self.size - 1 and col == self.size:
            return True

        if col == self.size:  
            row += 1
            col = 0

        if self.board[row, col] != 0:
            return self.__fill_board(row, col + 1)

        for num in self.rng.permutation(np.arange(1, self.size + 1)):
            if self.__is_safe(row, col, num):
                self.board[row, col] = num
                if self.__fill_board(row, col + 1):
                    return True
        
        self.board[row, col] = 0
        return False
    
    def __is_safe(self, row: int, col: int, num: int) -> bool:
        """
        Checks if it's safe to place a number in the given row and column.

        Args:
            row (int): The row to check.
            col (int): The column to check.
            num (int): The number to place.

        Returns:
            bool: True if it's safe to place the number, False otherwise.
        """

        if num in self.board[row, :] or num in self.board[:, col]:
            return False
        start_row, start_col = row - row % self.subgrid_size, col - col % self.subgrid_size
        if num in self.board[start_row:start_row + self.subgrid_size, start_col:start_col + self.subgrid_size]:
            return False
        return True

    def __valid_sudoku(self) -> bool:
        """
        Validates the generated Sudoku puzzle.

        Returns:
            bool: True if the Sudoku puzzle is valid, False otherwise.
        """

        sudoku_solver = SudokuChecker(self.board)
        return sudoku_solver.is_valid_solution()

    def __remove_cells(self) -> None:
        """
        Removes cells from the puzzle based on the difficulty level to create the final puzzle.
        """

        difficulty_levels: Dict[Difficulty, int] = {
            Difficulty.EASY: 20,
            Difficulty.MEDIUM: 35,
            Difficulty.HARD: 50
        }

        cells_to_remove: int = difficulty_levels.get(self.difficulty, 35)

        all_cells: List[Tuple[int, int]] = [(row, col) for row in range(self.size) for col in range(self.size)]
        self.rng.shuffle(all_cells)

        removed_count: int = 0
        for row, col in all_cells:
            original_value: int = self.board[row, col]
            self.board[row, col] = 0

            if not self.__has_unique_solution():
                self.board[row, col] = original_value
            else:
                removed_count += 1

            if removed_count >= cells_to_remove:
                break

    def __has_unique_solution(self) -> bool:
        """
        Checks if the current board configuration has a unique solution.

        Returns:
            bool: True if the puzzle has a unique solution, False otherwise.
        """

        solver = SudokuSolver(self.board)
        return solver.solve()

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if value < 1:
            return
        self._size = value
        self.board = np.zeros((self.size, self.size), dtype=int)

    @property
    def subgrid_size(self) -> int:
        return self._subgrid_size

    @subgrid_size.setter
    def subgrid_size(self, value: int) -> None:
        if value ** 2 != self.size:
            return
        self._subgrid_size = value

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: Difficulty) -> None:
        self._difficulty = value

    @property
    def board(self) -> np.ndarray:
        return self._board

    @board.setter
    def board(self, value: np.ndarray) -> None:
        if value.shape != (self.size, self.size):
            return
        self._board = value

    @property
    def rng(self) -> np.random.Generator:
        return self._rng

    @rng.setter
    def rng(self, value: np.random.Generator) -> None:
        self._rng = value

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()
