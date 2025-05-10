import pytest

from player import Player

# Pytest tests for Player class, converted from player.py doctests.

def test_initial_state():
    p = Player("test")
    assert p.name == "test"
    assert p.score == 0

def test_invalid_name_assignment():
    p = Player("test")
    p.name = 15
    assert p.name == "test"

def test_invalid_score_assignment():
    p = Player("test")
    p.score = "30"
    assert p.score == 0

def test_valid_name_assignment():
    p = Player("whatever")
    p.name = "15"
    assert p.name == "15"

def test_valid_score_assignment():
    p = Player("whatever")
    p.score = 30
    assert p.score == 30
