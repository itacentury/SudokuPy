from libs.game_state import GameState

# Pytest tests for GameState class, converted from game_state.py doctests.

def test_waiting_for_name_repr() -> None:
    """
    Test that the repr of WAITING_FOR_NAME matches the expected enum representation.
    """

    assert repr(GameState.WAITING_FOR_NAME) == "<GameState.WAITING_FOR_NAME: 1>"

def test_game_ready_value() -> None:
    """
    Test that the value of GAME_READY is 2.
    """

    assert GameState.GAME_READY.value == 2

def test_game_in_progress_name() -> None:
    """
    Test that the name of GAME_IN_PROGRESS is 'GAME_IN_PROGRESS'.
    """

    assert GameState.GAME_IN_PROGRESS.name == "GAME_IN_PROGRESS"

def test_construct_from_value_four() -> None:
    """
    Test that constructing GameState with 4 returns GAME_OVER.
    """

    assert GameState(4) is GameState.GAME_OVER
