from libs.highscores import HighScoreManager

# Pytest tests for HighScoreManager class, converted from highscores.py doctests.


def test_highscore_manager_instance() -> None:
    """
    Check instance of highscore manager.
    """

    manager = HighScoreManager()
    assert isinstance(manager, HighScoreManager)


def test_highscore_manager_dictionary() -> None:
    """
    Check if scores key is inside highscore dictionary.
    """

    manager = HighScoreManager()
    assert "scores" in manager.load_highscore()


def test_adding_highscore() -> None:
    """
    Check adding new highscore to highscore manager.
    """

    manager = HighScoreManager()
    manager.add_highscore("John Doe", 500, "easy")
    assert "John Doe" in str(manager.highscores["scores"])


def test_setting_highscores() -> None:
    """
    Check overriding highscore.
    """

    manager = HighScoreManager()
    highscore: dict[str, list[tuple[str, int, str]]] = {"test": [("one", 1, "1")]}
    manager.highscores = highscore
    assert manager.highscores == highscore
