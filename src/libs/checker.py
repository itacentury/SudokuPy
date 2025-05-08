import numpy as np

class SudokuChecker:
    """
    The SudokuChecker class is designed to validate Sudoku solutions. It takes a 2D numpy array representing
    a Sudoku grid as input. The class provides methods to check if the provided grid is a valid Sudoku solution,
    ensuring each row, column, and 3x3 subgrid contains unique numbers from 1 to the size of the grid.

    Attributes:
        grid (Board): The sudoku grid.
        size (int): The size of the grid.

    Methods:
        is_valid_solution(self) -> bool
        __is_unique(self, arr: np.ndarray) -> bool

    Examples:
        >>> import numpy as np
        >>> grid = np.array([[5, 3, 4, 6, 7, 8, 9, 1, 2],
        ...                   [6, 7, 2, 1, 9, 5, 3, 4, 8],
        ...                   [1, 9, 8, 3, 4, 2, 5, 6, 7],
        ...                   [8, 5, 9, 7, 6, 1, 4, 2, 3],
        ...                   [4, 2, 6, 8, 5, 3, 7, 9, 1],
        ...                   [7, 1, 3, 9, 2, 4, 8, 5, 6],
        ...                   [9, 6, 1, 5, 3, 7, 2, 8, 4],
        ...                   [2, 8, 7, 4, 1, 9, 6, 3, 5],
        ...                   [3, 4, 5, 2, 8, 6, 1, 7, 9]])
        >>> checker = SudokuChecker(grid)
        >>> checker.is_valid_solution()
        True
        >>> checker.size
        9
        >>> checker.grid = np.array([[1, 2], [3, 4]])
        >>> checker.size
        2
    """
    
    def __init__(self, grid: np.ndarray) -> None:
        """
        Initializes the class with a Sudoku grid.

        Args:
            grid (np.ndarray): A 2D numpy array representing the Sudoku grid.
        """

        self.grid: np.ndarray = grid
        self.size: int = len(grid)

    def is_valid_solution(self) -> bool:
        """
        Checks if the current Sudoku grid is a valid solution.

        Returns:
            bool: True if the solution is valid, False otherwise.

        Examples:
            >>> grid = np.array([[5, 3, 4, 6, 7, 8, 9, 1, 2],
            ...                   [6, 7, 2, 1, 9, 5, 3, 4, 8],
            ...                   [1, 9, 8, 3, 4, 2, 5, 6, 7],
            ...                   [8, 5, 9, 7, 6, 1, 4, 2, 3],
            ...                   [4, 2, 6, 8, 5, 3, 7, 9, 1],
            ...                   [7, 1, 3, 9, 2, 4, 8, 5, 6],
            ...                   [9, 6, 1, 5, 3, 7, 2, 8, 4],
            ...                   [2, 8, 7, 4, 1, 9, 6, 3, 5],
            ...                   [3, 4, 5, 2, 8, 6, 1, 7, 9]])
            >>> checker = SudokuChecker(grid)
            >>> checker.is_valid_solution()
            True
            >>> grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ...                  [0, 0, 0, 0, 0, 0, 0, 0, 0]])
            >>> checker = SudokuChecker(grid)
            >>> checker.is_valid_solution()
            False
        """

        for row in range(self.size):
            if not self.__is_unique(self.grid[row, :]):
                return False
        
        for col in range(self.size):
            if not self.__is_unique(self.grid[:, col]):
                return False
        
        for row in range(0, self.size, 3):
            for col in range(0, self.size, 3):
                if not self.__is_unique(self.grid[row:row + 3, col:col + 3].flatten()):
                    return False
        
        return True
    
    def __is_unique(self, arr: np.ndarray) -> bool:
        """
        Checks if all elements in an array are unique and form a sequence from 1 to the size of the Sudoku board.

        Args:
            arr (np.ndarray): The array to check.

        Returns:
            bool: True if the array contains a sequence from 1 to the size of the board, False otherwise.
        """

        return np.array_equal(np.sort(arr), np.arange(1, self.size + 1))
    
    @property
    def grid(self) -> np.ndarray:
        return self._board

    @grid.setter
    def grid(self, value: np.ndarray) -> None:
        """
        Examples:
            >>> checker = SudokuChecker(np.array([[5, 6], [7, 8]]))
            >>> checker.grid
            array([[5, 6],
                    [7, 8]])
            >>> checker.size
            2
        """

        self._board = value
        self._size = len(value)

    @property
    def size(self) -> int:
        return self._size
    
    @size.setter
    def size(self, value: int) -> None:
        """
        Examples:
            >>> checker = SudokuChecker(np.array([[5, 6], [7, 8]]))
            >>> checker.size = 2
            >>> checker.size
            2
            >>> check.size = -3
            >>> checker.size
            2
        """

        if value < 1:
            return
        self._size = value

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()