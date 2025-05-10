from player import Player

# Pytest tests for Player class, converted from player.py doctests.

def test_initial_state() -> None:
    """
    Test that a new Player has the correct name and a score of zero.
    """
    
    p = Player("test")
    assert p.name == "test"
    assert p.score == 0

def test_invalid_name_assignment() -> None:
    """
    Test that assigning a non-string value to name does not change the existing name.
    """

    p = Player("test")
    p.name = 15
    assert p.name == "test"

def test_invalid_score_assignment() -> None:
    """
    Test that assigning a non-integer value to score does not change the existing score.
    """

    p = Player("test")
    p.score = "30"
    assert p.score == 0

def test_valid_name_assignment() -> None:
    """
    Test that assigning a valid string to name updates the name correctly.
    """

    p = Player("test")
    p.name = "15"
    assert p.name == "15"

def test_valid_score_assignment() -> None:
    """
    Test that assigning a valid integer to score updates the score correctly.
    """

    p = Player("test")
    p.score = 30
    assert p.score == 30
