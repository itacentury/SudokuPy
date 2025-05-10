class Cursor:
    """
    The Cursor class represents a cursor's position with x and y coordinates.
    The coordinates must be integers. The class provides properties for accessing
    and setting these coordinates, ensuring that only integer values are accepted.

    Attributes:
        x (int): The x-coordinate of the cursor. Non-integer values are ignored, and negative values are reset to 0.
        y (int): The y-coordinate of the cursor. Similar to `x`, non-integer and negative values are not accepted.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the Cursor class.
        """
        
        self.x: int = 0
        self.y: int = 0

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int):
            return
        if value < 0:
            return
        self._x = value

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int):
            return
        if value < 0:
            return
        self._y = value

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()