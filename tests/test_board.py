import numpy as np

from libs.board import Board

# Pytest tests for Board class, converted from board.py doctests.

def test_board_initialization_and_defaults() -> None:
    """
    Test correct initialization of Board and default attribute values.
    """
    
    grid: np.ndarray = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = Board(grid, None)
    assert (b.cursor.x, b.cursor.y) == (0, 0)
    np.testing.assert_array_equal(b.grid, grid)
    np.testing.assert_array_equal(b.reset_grid, grid)
    assert b.current_key == 9
    assert b.highlighted_number == 0

    b2 = Board(grid, None)
    b2.grid[0, 1] = 5
    expected_grid: np.ndarray = np.array([[1, 5, 3],
                              [4, 5, 6],
                              [7, 8, 9]])
    np.testing.assert_array_equal(b2.grid, expected_grid)
    expected_reset: np.ndarray = np.array([[1, 2, 3],
                               [4, 5, 6],
                               [7, 8, 9]])
    np.testing.assert_array_equal(b2.reset_grid, expected_reset)

def test_grid_property_does_not_affect_reset_grid() -> None:
    """
    Ensure modifications to grid do not affect reset_grid.
    """

    grid: np.ndarray = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = Board(grid, None)
    np.testing.assert_array_equal(b.grid, grid)
    np.testing.assert_array_equal(b.reset_grid, grid)
    b.grid[1, 1] = 0
    expected_grid: np.ndarray = np.array([[1, 2, 3],
                              [4, 0, 6],
                              [7, 8, 9]])
    expected_reset_grid: np.ndarray = np.array([[1, 2, 3],
                              [4, 5, 6],
                              [7, 8, 9]])
    np.testing.assert_array_equal(b.grid, expected_grid)
    np.testing.assert_array_equal(b.reset_grid, expected_reset_grid)

def test_reset_grid_property_does_not_affect_grid() -> None:
    """
    Ensure modifications to reset_grid do not affect grid.
    """

    grid: np.ndarray = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = Board(grid, None)
    np.testing.assert_array_equal(b.reset_grid, grid)
    np.testing.assert_array_equal(b.grid, grid)
    b.reset_grid[1, 1] = 0
    expected_reset: np.ndarray = np.array([[1, 2, 3],
                               [4, 0, 6],
                               [7, 8, 9]])
    np.testing.assert_array_equal(b.reset_grid, expected_reset)
    np.testing.assert_array_equal(b.grid, grid)

def test_current_key_setter_validation() -> None:
    """
    Validate that current_key setter enforces allowed value ranges.
    """

    grid: np.ndarray = np.zeros((3, 3), dtype=int)
    b = Board(grid, None)
    assert b.current_key == 9
    b.current_key = 15
    assert b.current_key == 9
    b.current_key = 100
    assert b.current_key == 100
    b.current_key = 199
    assert b.current_key == 100
    b.current_key = 259
    assert b.current_key == 259
    b.current_key = 354
    assert b.current_key == 259

def test_highlighted_number_setter_validation() -> None:
    """
    Validate that highlighted_number setter enforces allowed number ranges.
    """

    grid: np.ndarray = np.zeros((3, 3), dtype=int)
    b = Board(grid, None)
    assert b.highlighted_number == 0
    b.highlighted_number = 5
    assert b.highlighted_number == 5
    b.highlighted_number = -13
    assert b.highlighted_number == 5
    b.highlighted_number = 9478
    assert b.highlighted_number == 5
    b.highlighted_number = 9
    assert b.highlighted_number == 9
