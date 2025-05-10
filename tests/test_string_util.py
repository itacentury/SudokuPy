import pytest

from libs.string_util import StringUtil

# Pytest tests for StringUtil class, converted from string_util.py doctests.


def test_shorten_string_without_truncation_when_length_less_or_equal() -> None:
    """
    Test that a string shorter than or equal to max_length is returned unchanged.
    """

    assert StringUtil.shorten_string("abcdefg", 7) == "abcdefg"
    assert StringUtil.shorten_string("hi", 5) == "hi"


def test_shorten_string_for_even_max_length() -> None:
    """
    Test that shortening works correctly when max_length is even.
    """

    assert StringUtil.shorten_string("Hello, World!", 12) == "Hello..orld!"


def test_shorten_string_for_odd_max_length() -> None:
    """
    Test that shortening works correctly when max_length is odd.
    """

    assert StringUtil.shorten_string("Hello, World!", 5) == "He..!"
    assert StringUtil.shorten_string("abcdefg", 5) == "ab..g"


def test_shorten_string_max_length_less_than_three_raises() -> None:
    """
    Test that providing max_length less than 3 raises a ValueError.
    """

    with pytest.raises(ValueError):
        StringUtil.shorten_string("test", 2)
    with pytest.raises(ValueError):
        StringUtil.shorten_string("a", 0)
