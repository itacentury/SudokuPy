import sys
import json
import time
import curses
import tkinter as tk

from tkinter import filedialog
from typing import Literal
from collections.abc import Callable

from player import Player
from user_interface import UI
from libs.generator import SudokuGenerator
from libs.board import Board
from libs.highscores import HighScoreManager
from libs.checker import SudokuChecker
from libs.difficulty import Difficulty


class Game:
    """
    Represents a game session with functionalities to manage game states, player interactions, and AI switches.

    Attributes:
        ui (Optional[UI]): The user interface for the game, initially None.
        player (Optional[Player]): The player of the game, initially None.
        board (Optional[Board]): The game board, initially None.
        hs_manager (HighScoreManager): Manages high scores for the game.
        generator (SudokuGenerator): Generates Sudoku puzzles based on difficulty.
        difficulty (Difficulty): The difficulty level of the game.

    Methods:
        set_player(self, player: Player) -> None
        __save_game_state(self) -> None
        __game_to_json(self) -> Dict[str, any]
        __load_game_state(self) -> None
        __switch_to_ai(self) -> None
        step(self, key: int) -> None
        __handle_key_actions(self, key: int) -> None
        __move_cursor(self, axis: Literal["x", "y"], delta: Literal[1, -1]) -> None
        __reset_board(self) -> None
        __incr_highlighted_num(self) -> None
        __decr_highlighted_num(self) -> None
        __check_solution(self) -> None
        __finish_game(self) -> None
        __process_num_input(self, number: int) -> None
        run(self) -> None
    """

    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM) -> None:
        """
        Initializes a new game instance with the specified difficulty.

        Args:
            difficulty (Difficulty): The difficulty setting for the game, defaults to Difficulty.MEDIUM.
        """

        self.ui: UI | None = None
        self.player: Player | None = None
        self.board: Board | None = None
        self.hs_manager: HighScoreManager = HighScoreManager()
        self.generator = SudokuGenerator(difficulty=difficulty)
        self.difficulty: Difficulty = difficulty

    def set_player(self, player: Player) -> None:
        """
        Sets the player for the game.

        Args:
            player (Player): The player to set for the game.
        """

        self.player = player

    def __save_game_state(self) -> None:
        """
        Saves the current game state to a file selected by the user.
        """

        root = tk.Tk()
        root.withdraw()

        file_path: str = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select location to save your game",
            filetypes=[("json files", "*.json")],
            defaultextension=".json",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(self.__game_to_json(), file)
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
        except PermissionError:
            print(f"Error: Permission denied to read '{file_path}'")
        except TypeError as e:
            print(f"Error serializing game state to JSON: {e}")
        except OSError as e:
            print(f"I/O error while writing '{file_path}': {e}")

    def __game_to_json(self) -> dict[str, any]:
        """
        Serializes the current game state into a dictionary.

        This method gathers essential information about the current game state,
        including the player's name, start time, current time (as saved time),
        and the state of the game board.

        Returns:
            Dict[str, any]: A dictionary representing the current game state,
                            with keys for the player's name, difficulty, start time,
                            saved time, and the state of the game board.
        """

        game_state: dict[str, any] = {
            "name": self.player.name,
            "difficulty": str(self.board.difficulty),
            "start_time": self.ui.drawing.start_time,
            "saved_time": time.time(),
            "board": self.board.to_json(),
        }

        return game_state

    def __load_game_state(self) -> None:
        """
        Loads a game state from a file selected by the user.
        """

        root = tk.Tk()
        root.withdraw()

        file_path: str = filedialog.askopenfilename(
            initialdir="/",
            title="Select game file to load",
            filetypes=[("json files", "*.json")],
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data: dict[str, any] = json.load(file)
            self.player.name = data["name"]
            self.difficulty = Difficulty.from_str(data["difficulty"])
            self.board.difficulty = Difficulty.from_str(data["difficulty"])
            self.ui.drawing.start_time = data["start_time"] + (
                time.time() - data["saved_time"]
            )
            self.board.from_json(data["board"])
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
        except PermissionError:
            print(f"Error: Permission denied to read '{file_path}'")
        except TypeError as e:
            print(f"Error serializing game state to JSON: {e}")
        except OSError as e:
            print(f"I/O error while reading '{file_path}': {e}")

    def __switch_to_ai(self) -> None:
        """
        Switches the game mode to AI player.
        """

        self.ui.is_ai_player = True
        self.ui.drawing.draw_ai_player_notice()

    def step(self, key: int) -> None:
        """
        Processes a single step in the game based on the key pressed.

        Args:
            key (int): The key code of the pressed key.
        """

        if key == ord("q"):
            self.__finish_game()
            return

        self.__handle_key_actions(key)

    def __handle_key_actions(self, key: int) -> None:
        """
        Handles actions based on the key pressed.

        Args:
            key (int): The key code of the pressed key.
        """

        cursor_actions: dict[
            int, Callable[[Literal["x", "y"], Literal[1, -1]], None]
        ] = {
            curses.KEY_UP: lambda: self.__move_cursor("y", -1),
            curses.KEY_DOWN: lambda: self.__move_cursor("y", 1),
            curses.KEY_LEFT: lambda: self.__move_cursor("x", -1),
            curses.KEY_RIGHT: lambda: self.__move_cursor("x", 1),
        }

        if key in cursor_actions:
            cursor_actions[key]()

        special_actions: dict[int, Callable[[None], None]] = {
            ord("r"): lambda: self.__reset_board(),
            ord("R"): lambda: self.__reset_board(),
            ord("c"): lambda: self.__check_solution(),
            ord("C"): lambda: self.__check_solution(),
            ord("+"): lambda: self.__incr_highlighted_num(),
            ord("-"): lambda: self.__decr_highlighted_num(),
            ord("s"): lambda: self.__save_game_state(),
            ord("S"): lambda: self.__save_game_state(),
            ord("l"): lambda: self.__load_game_state(),
            ord("L"): lambda: self.__load_game_state(),
            ord("a"): lambda: self.__switch_to_ai(),
            ord("A"): lambda: self.__switch_to_ai(),
        }

        if key in special_actions:
            special_actions[key]()

        if 48 <= key <= 58:
            self.__process_num_input(int(chr(key)))

    def __move_cursor(self, axis: Literal["x", "y"], delta: Literal[1, -1]) -> None:
        """
        Moves the cursor on the board.

        Args:
            axis (Literal["x", "y"]): The axis along which to move the cursor.
            delta (Literal[1, -1]): The direction and magnitude of the movement.
        """

        if axis == "x":
            self.board.cursor.x = min(max(0, self.board.cursor.x + delta), 8)
        elif axis == "y":
            self.board.cursor.y = min(max(0, self.board.cursor.y + delta), 8)

    def __reset_board(self) -> None:
        """
        Resets the game board to its initial state.
        """

        self.board.grid = self.board.reset_grid.copy()

    def __incr_highlighted_num(self) -> None:
        """
        Increments the highlighted number on the board.
        """

        self.board.highlighted_number += 1

    def __decr_highlighted_num(self) -> None:
        """
        Decrements the highlighted number on the board.
        """

        self.board.highlighted_number -= 1

    def __check_solution(self) -> None:
        """
        Checks if the current solution on the board is correct.
        """

        checker = SudokuChecker(self.board.grid)
        score = self.player.score

        self.ui.drawing.timer_paused = True
        self.ui.drawing.pause_start_time = time.time()

        if checker.is_valid_solution():
            self.ui.drawing.draw_game_over(score)
            self.__finish_game()

        self.ui.drawing.draw_game_continue(score)

        self.ui.drawing.timer_paused = False
        self.ui.drawing.start_time += time.time() - self.ui.drawing.pause_start_time
        self.ui.drawing.pause_start_time = 0.0

    def __finish_game(self) -> None:
        """
        Finishes the game and exits.
        """

        if self.player and self.player.score > 0:
            self.hs_manager.add_highscore(
                self.player.name, self.player.score, self.difficulty
            )
        self.hs_manager.save_highscore()
        sys.exit(0)

    def __process_num_input(self, number: int) -> None:
        """
        Processes number input from the user.

        Args:
            number (int): The number input by the user.
        """

        if self.board.reset_grid[self.board.cursor.y, self.board.cursor.x]:
            return
        self.board.grid[self.board.cursor.y, self.board.cursor.x] = number

    def run(self) -> None:
        """
        Starts and runs the game.
        """

        self.board = Board(self.generator.generate(), self.difficulty)
        ui = UI(self, self.board)
        self.ui = ui

        curses.wrapper(ui.wait_for_input, self.hs_manager)
