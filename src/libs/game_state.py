from enum import Enum

class GameState(Enum):
    """
    Represents the possible states of a game session.

    Examples:
        >>> GameState.WAITING_FOR_NAME
        <GameState.WAITING_FOR_NAME: 1>
        >>> GameState.GAME_READY.value
        2
        >>> GameState.GAME_IN_PROGRESS.name
        'GAME_IN_PROGRESS'
        >>> GameState(4)
        <GameState.GAME_OVER: 4>
    """

    WAITING_FOR_NAME = 1
    GAME_READY = 2
    GAME_IN_PROGRESS = 3
    GAME_OVER = 4

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()