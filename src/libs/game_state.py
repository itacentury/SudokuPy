from enum import Enum


class GameState(Enum):
    """
    Represents the possible states of a game session.
    """

    WAITING_FOR_NAME = 1
    GAME_READY = 2
    GAME_IN_PROGRESS = 3
    GAME_OVER = 4
