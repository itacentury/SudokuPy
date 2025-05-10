class Player:
    """
    The Player class represents a player. It stores the player's name and score.
    The name must be a string, and the score must be an integer. The class provides properties
    for accessing and validating these attributes to ensure that only valid values are set.

    Attributes:
        name (str): The name of the player.
        score (int): The score of the player.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.score: int = 0

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            return
        self._name = value

    @property
    def score(self) -> int:
        return self._score
    
    @score.setter
    def score(self, value: int) -> None:
        if not isinstance(value, int):
            return
        self._score = value
