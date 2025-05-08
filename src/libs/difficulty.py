from enum import Enum

class Difficulty(Enum):
    """
    Represents the difficulty levels of a game with three levels: easy, medium, and hard.
    Each level is associated with a numeric value and a string label.

    Attributes:
        num (int): The number corresponding to the enum value.
        label (str): The label to the corresponding enum value.

    Examples:
        >>> Difficulty.EASY
        <Difficulty.EASY: (1, 'easy')>
        >>> str(Difficulty.MEDIUM)
        'medium'
        >>> Difficulty.HARD.num
        3
        >>> Difficulty.from_str("easy")
        <Difficulty.EASY: (1, 'easy')>
        >>> Difficulty.from_str("unknown")
        <Difficulty.MEDIUM: (2, 'medium')>
        >>> Difficulty.from_str("hard") == Difficulty.HARD
        True
    """

    EASY = (1, "easy")
    MEDIUM = (2, "medium")
    HARD = (3, "hard")
    
    def __init__(self, num: int, label: str) -> None:
        """
        Initializes a new instance of the Difficulty enum.
        
        Args:
            num (int): The numeric value associated with the difficulty level.
            label (str): The string label representing the difficulty level.
        """
        
        self.num: int = num
        self.label: str = label

    def __str__(self) -> str:
        """
        Returns the string label of the difficulty level.

        Returns:
            str: The label of the difficulty.
        """
                
        return self.label
    
    @staticmethod
    def from_str(label: str) -> "Difficulty":
        """
        Returns the Difficulty enum member matching the given label.
        Defaults to MEDIUM if the label does not match any difficulty level.

        Args:
            label (str): The string label of the difficulty level to match.

        Returns:
            Difficulty: The matching Difficulty enum member.

        Examples:
            >>> Difficulty.from_str("easy")
            <Difficulty.EASY: (1, 'easy')>
            >>> Difficulty.from_str("medium")
            <Difficulty.MEDIUM: (2, 'medium')>
            >>> Difficulty.from_str("hard")
            <Difficulty.HARD: (3, 'hard')>
            >>> Difficulty.from_str("unknown")
            <Difficulty.MEDIUM: (2, 'medium')>
        """

        if label == "easy":
            return Difficulty.EASY
        elif label == "medium":
            return Difficulty.MEDIUM
        elif label == "hard":
            return Difficulty.HARD
        else:
            return Difficulty.MEDIUM

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()