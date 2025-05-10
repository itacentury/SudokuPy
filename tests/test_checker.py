import numpy as np

from libs.checker import SudokuChecker

def test_valid_sudoku_solution() -> None:
    """
    Test that a known valid 9x9 Sudoku grid is considered a valid solution.
    """

    grid: np.ndarray = np.array([
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ])
    checker = SudokuChecker(grid)
    assert checker.is_valid_solution() is True
    assert checker.size == 9

def test_invalid_sudoku_solution_all_zeros() -> None:
    """
    Test that an all-zero 9x9 grid is not considered a valid Sudoku solution.
    """

    grid: np.ndarray = np.zeros((9, 9), dtype=int)
    checker = SudokuChecker(grid)
    assert checker.is_valid_solution() is False
    assert checker.size == 9

def test_grid_property_and_size_update() -> None:
    """
    Test that assigning a new grid updates both the grid and the size properties.
    """

    initial: np.ndarray = np.array([[5, 6], [7, 8]])
    checker = SudokuChecker(initial)
    assert np.array_equal(checker.grid, initial)
    assert checker.size == 2

    new_grid: np.ndarray = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    checker.grid = new_grid
    assert np.array_equal(checker.grid, new_grid)
    assert checker.size == 3

def test_size_setter_rejects_invalid_values() -> None:
    """
    Test that setting size to a negative value is ignored and size remains unchanged.
    """

    grid: np.ndarray = np.array([[1]])
    checker = SudokuChecker(grid)
    assert checker.size == 1

    checker.size = -5
    assert checker.size == 1
