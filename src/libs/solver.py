import numpy as np

from typing import Tuple

class SudokuSolver:
    """
    A class to solve a Sudoku puzzle using backtracking.

    Attributes:
        board (np.ndarray): A 2D numpy array representing the Sudoku board.
        size (int): The size of the Sudoku board (e.g., 9 for a standard Sudoku).

    Methods:
        solve(self) -> bool
        __find_empty_cell(self) -> Tuple[int, int] | Tuple[None, None]
        __is_valid(self, row: int, col: int, num: int) -> bool

    Examples:
        >>> board = np.array([
        ...     [5, 3, 0, 0, 7, 0, 0, 0, 0],
        ...     [6, 0, 0, 1, 9, 5, 0, 0, 0],
        ...     [0, 9, 8, 0, 0, 0, 0, 6, 0],
        ...     [8, 0, 0, 0, 6, 0, 0, 0, 3],
        ...     [4, 0, 0, 8, 0, 3, 0, 0, 1],
        ...     [7, 0, 0, 0, 2, 0, 0, 0, 6],
        ...     [0, 6, 0, 0, 0, 0, 2, 8, 0],
        ...     [0, 0, 0, 4, 1, 9, 0, 0, 5],
        ...     [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ... ])
        >>> solver = SudokuSolver(board)
        >>> solver.solve()
        True
        >>> isinstance(solver.board, np.ndarray) and solver.board.shape == (9, 9)
        True
    """

    def __init__(self, board: np.ndarray) -> None:
        """
        Initializes the SudokuSolver with a Sudoku board.

        Args:
            board (np.ndarray): A 2D numpy array representing the Sudoku board.
        """

        self.board: np.ndarray = board.copy()
        self.size: int = len(board)

    def solve(self) -> bool:
        """
        Attempts to solve the Sudoku puzzle using backtracking.

        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """

        row, col = self.__find_empty_cell()
        if row is None:
            return True

        for num in range(1, self.size + 1):
            if self.__is_valid(row, col, num):
                self.board[row, col] = num
                if self.solve():
                    return True
                self.board[row, col] = 0

        return False

    def __find_empty_cell(self) -> Tuple[int, int] | Tuple[None, None]:
        """
        Finds the next empty cell (0) on the board.

        Returns:
            Tuple[int, int] | Tuple[None, None]: The row and column of the next empty cell, or (None, None) if no empty cells are left.
        """

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row, col] == 0:
                    return row, col
        return None, None

    def __is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if placing a number in the given row and column is valid according to Sudoku rules.

        Args:
            row (int): The row in which to check.
            col (int): The column in which to check.
            num (int): The number to place.

        Returns:
            bool: True if the number can be placed, False otherwise.
        """

        if num in self.board[row, :]:
            return False
        if num in self.board[:, col]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.board[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()