import numpy as np

from libs.generator import SudokuGenerator
from libs.difficulty import Difficulty

# Pytest tests for SudokuGenerator class, converted from generator.py doctests.


def test_generated_puzzle_instance() -> None:
    """
    Check instance of generated puzzle.
    """

    generator = SudokuGenerator(difficulty=Difficulty.EASY)
    puzzle = generator.generate()
    assert isinstance(puzzle, np.ndarray)


def test_generated_puzzle_shape() -> None:
    """
    Check shape of generated puzzle.
    """

    generator = SudokuGenerator(difficulty=Difficulty.EASY)
    puzzle = generator.generate()
    assert puzzle.shape == (9, 9)
