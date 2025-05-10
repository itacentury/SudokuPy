import pytest
import numpy as np

from game import Game
from libs.board import Board
from user_interface import UI
from libs.game_state import GameState
from libs.difficulty import Difficulty

# Pytest tests for UI class, converted from user_interface.py doctests.


def test_ui_initial_state_waiting_for_name_and_not_ai() -> None:
    """
    Test that UI starts in the WAITING_FOR_NAME state and AI control is off.
    """

    board = Board(np.array([[5, 6], [7, 8]]), Difficulty.MEDIUM)
    game = Game()
    ui = UI(game, board)
    assert ui.game_state == GameState.WAITING_FOR_NAME
    assert ui.is_ai_player is False


@pytest.mark.parametrize(
    "initial_state",
    [
        GameState.WAITING_FOR_NAME,
    ],
)
def test_ui_has_drawing_none_before_start(initial_state: GameState) -> None:
    """
    Test that before entering the input loop, the drawing attribute is still None
    and the game_state matches the expected initial state.
    """

    board = Board(np.array([[1]]), Difficulty.MEDIUM)
    game = Game()
    ui = UI(game, board)
    assert ui.drawing is None
    assert ui.game_state == initial_state
