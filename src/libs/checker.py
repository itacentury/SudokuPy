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
        self._board = value
        self._size = len(value)

    @property
    def size(self) -> int:
        return self._size
    
    @size.setter
    def size(self, value: int) -> None:
        if value < 1:
            return
        self._size = value

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()
