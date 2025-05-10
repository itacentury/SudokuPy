from libs.cursor import Cursor

# Pytest tests for Cursor class, converted from cursor.py doctests.


def test_initial_position() -> None:
    """
    Test that a new Cursor starts at (0, 0).
    """

    c = Cursor()
    assert c.x == 0
    assert c.y == 0


def test_valid_x_and_negative_y_assignment() -> None:
    """
    Test that assigning a valid integer to x updates it and negative y is ignored (remains 0).
    """

    c = Cursor()
    c.x = 5
    c.y = -3
    assert c.x == 5
    assert c.y == 0


def test_non_integer_assignments_are_ignored() -> None:
    """
    Test that assigning non-integer values to x or y leaves previous values unchanged.
    """

    c = Cursor()
    c.x = 5
    c.y = 0
    c.x = "13"
    c.y = 2.7
    assert c.x == 5
    assert c.y == 0
