import curses
import random

from typing import Tuple

from libs.board import Board

class AiPlayer:
    """
    An AI player class that calculates automatic moves on a game board.

    Methods:
        calc_move(self) -> int
        __find_nearest_empty_cell(self) -> Tuple[int, int]
        __is_valid(self, row: int, col: int, num: int) -> bool

    Attributes:
        board (Board): The sudoku board.
        size (int): The size of the board.
    """

    def __init__(self, board: Board) -> None:
        """
        Initializes a new instance of the AiPlayer class.

        Args:
            board (Board): The current sudoku board.
        """

        self.board: Board = board
        self.size: int = len(board.grid)

    def calc_move(self) -> int:
        """
        Calculates the AI's next move.

        Returns:
            int: The key to be pressed to perform the next move. This can be an arrow key (for movement),
                 a number (for placement), or 'c' (as ASCII value) if no valid move was found.
        """

        y, x = self.__find_nearest_empty_cell()
        if y is None or x is None:
            return ord('c')
        
        if self.board.cursor.x != x or self.board.cursor.y != y:
            if x - self.board.cursor.x > 0:
                return curses.KEY_RIGHT
            elif x - self.board.cursor.x < 0:
                return curses.KEY_LEFT
            
            if y - self.board.cursor.y > 0:
                return curses.KEY_DOWN
            elif y - self.board.cursor.y < 0:
                return curses.KEY_UP

        for num in random.sample(range(1, self.size + 1), self.size):
            if self.__is_valid(y, x, num):
                self.board.highlighted_number = num
                return ord(str(num))

        return ord('c')
    
    def __find_nearest_empty_cell(self) -> Tuple[int, int]:
        """
        Finds the nearest empty cell relative to the cursor.

        Returns:
            Tuple[int, int]: The coordinates of the nearest empty cell or (None, None) if none was found.
        """

        min_distance: float = float('inf')
        nearest_cell: Tuple[int, int] = (None, None)

        for row in range(self.size):
            for col in range(self.size):
                if self.board.grid[row, col] == 0:
                    distance = abs(self.board.cursor.x - col) + abs(self.board.cursor.y - row)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_cell = (row, col)
        return nearest_cell
    
    def __is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if a number can be placed at a given position.

        Args:
            row (int): The row position.
            col (int): The column position.
            num (int): The number to be placed.

        Returns:
            bool: True if the number can be placed, False otherwise.
        """
        
        if num in self.board.grid[row, :]:
            return False
        if num in self.board.grid[:, col]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.board.grid[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True

def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()