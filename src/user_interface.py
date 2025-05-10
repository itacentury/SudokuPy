import time
import curses
import threading

from typing import Optional

from player import Player
from ai_player import AiPlayer
from libs.drawing import Drawing
from libs.board import Board
from libs.highscores import HighScoreManager
from libs.game_state import GameState

class UI:
    """
    A class to manage the user interface of the game.

    Attributes:
        board (Board): The game board.
        game (Game): The game logic handler.
        drawing (Optional[Drawing]): The drawing handler for the game UI.
        game_state (GameState): The current state of the game.
        is_ai_player (bool): Flag to determine if the current player is an AI.
        ai_player (AiPlayer): The AI player instance.

    Methods:
        wait_for_input(self, stdscr: curses.window, manager: HighScoreManager) -> None
        __draw_and_update(self, stdscr: curses.window) -> None
        __handle_input(self, stdscr: curses.window) -> None
        __get_player_name(self) -> None
    """

    def __init__(self, game, board: Board) -> None:
        """
        Initializes the UI with the game and board instances.

        Args:
            game (Game): An instance of the game logic.
            board (Board): The game board to be used.
        """

        from game import Game

        self.board: Board = board
        self.game: Game = game
        self.drawing: Optional[Drawing] = None
        self.game_state = GameState.WAITING_FOR_NAME
        self.is_ai_player: bool = False
        self.ai_player: AiPlayer = AiPlayer(board)

    def wait_for_input(self, stdscr: curses.window, manager: HighScoreManager) -> None:
        """
        Main loop waiting for user input and updating the game state accordingly.

        Args:
            stdscr (curses.window): The standard screen provided by curses for drawing.
            manager (HighScoreManager): The high score manager instance.
        """

        self.drawing = Drawing(self.board, stdscr, manager)
        clock_thread: threading.Thread | None = None

        while True:
            self.__draw_and_update(stdscr)

            if self.game_state == GameState.WAITING_FOR_NAME:
                self.__get_player_name()
                self.game_state = GameState.GAME_READY
            elif self.game_state == GameState.GAME_READY:
                self.drawing.draw_start_game()
                self.board.current_key = stdscr.getch()
                self.game_state = GameState.GAME_IN_PROGRESS
                stdscr.clear()
                stdscr.refresh()
            elif self.game_state == GameState.GAME_IN_PROGRESS:
                if clock_thread is None:
                    clock_thread = threading.Thread(target=self.drawing.draw_clock, daemon=True)
                    clock_thread.start()

                self.__handle_input(stdscr)

    def __draw_and_update(self, stdscr: curses.window) -> None:
        """
        Draws the current state of the game and updates the screen.

        Args:
            stdscr (curses.window): The standard screen provided by curses for drawing.
        """

        self.drawing.draw()
        stdscr.refresh()

    def __handle_input(self, stdscr: curses.window) -> None:
        """
        Handles the user input during the game.

        Args:
            stdscr (curses.window): The standard screen provided by curses for drawing.
        """

        key: int = -1
        if self.is_ai_player:
            key = self.ai_player.calc_move()
            if key == ord('c'):
                self.is_ai_player = False
                time.sleep(2.5)
            time.sleep(0.25)
        else:
            key = stdscr.getch()
        self.board.current_key = key
        self.game.step(self.board.current_key)

    def __get_player_name(self) -> None:
        """
        Prompts the user for their name and updates the game and drawing instances with the new player.
        """
        
        name: str = self.drawing.draw_name_input()
        player = Player(name)
        self.game.set_player(player)
        self.drawing.set_player(player)
            
def main() -> None:
    import doctest
    doctest.testmod(verbose=True)

if __name__ == '__main__':
    main()
