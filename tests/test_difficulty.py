import pytest

from libs.difficulty import Difficulty

# Pytest tests for Difficulty class, converted from difficulty.py doctests.


def test_easy_enum_member_and_repr() -> None:
    """
    Test that Difficulty.EASY has the correct value tuple and its repr shows this value.
    """

    assert Difficulty.EASY.value == (1, "easy")
    assert repr(Difficulty.EASY) == "<Difficulty.EASY: (1, 'easy')>"


def test_str_medium_returns_label() -> None:
    """
    Test that converting Difficulty.MEDIUM to string yields its label.
    """

    assert str(Difficulty.MEDIUM) == "medium"


def test_hard_num_property() -> None:
    """
    Test that the num attribute of Difficulty.HARD equals 3.
    """

    assert Difficulty.HARD.num == 3


@pytest.mark.parametrize(
    "label, expected",
    [
        ("easy", Difficulty.EASY),
        ("medium", Difficulty.MEDIUM),
        ("hard", Difficulty.HARD),
        ("unknown", Difficulty.MEDIUM),
    ],
)
def test_from_str_various_labels(label: str, expected: Difficulty) -> None:
    """
    Test that Difficulty.from_str returns the correct enum member for valid labels,
    and defaults to MEDIUM for unrecognized labels.
    """

    assert Difficulty.from_str(label) is expected
