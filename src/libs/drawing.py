import curses
import time
from dataclasses import dataclass

from player import Player
from libs.board import Board
from libs.highscores import HighScoreManager
from libs.string_util import StringUtil


@dataclass(frozen=True)
class Origin:
    y: int
    x: int


@dataclass(frozen=True)
class Cell:
    row: int
    col: int
    num: int
    color_pair: int


class Drawing:
    """
    This class is responsible for handling all drawing operations within a curses terminal for a Sudoku game.
    It utilizes the curses library to draw the game board, player information, and high scores in a terminal window.

    Methods:
        set_player(self, player: Player) -> None
        draw(self) -> None
        __init_color_pairs(self) -> None
        __get_color_pair(self, x: int, y: int, num: int, board: Board) -> int
        draw_name_input(self) -> str
        __draw_cell(self, origin: Origin, cell: Cell) -> None
        __draw_grid(self) -> None
        draw_start_game(self) -> None
        draw_clock(self) -> None
        __draw_info_and_status(self) -> None
        __draw_controls(self) -> None
        __draw_highscores(self) -> None
        __draw_cursor(self) -> None
        draw_ai_player_notice(self) -> None
        draw_game_over(self, score: int) -> None
        draw_game_continue(self, score: int) -> None

    Attributes:
        board (Board): An instance of the Board class representing the Sudoku game board.
        hs_manager (HighScoreManager): An instance of the HighScoreManager class for managing high scores.
        player (Optional[Player]): An optional Player instance representing the current player. Defaults to None.
        stdscr (curses.window): The main window object provided by curses for drawing operations.
    """

    def __init__(
        self, board: Board, stdscr: curses.window, manager: HighScoreManager
    ) -> None:
        """
        Initializes the Drawing class with the game board, the standard screen window, and the high score manager.

        Parameters:
            board (Board): The game board to be drawn.
            stdscr (curses.window): The main curses window for drawing operations.
            manager (HighScoreManager): The high score manager for tracking and displaying high scores.
        """

        self.board: Board = board
        self.hs_manager: HighScoreManager = manager
        self.player: Player | None = None
        self.stdscr: curses.window = stdscr

        self.timer_paused: bool = False
        self.start_time: float = 0.0
        self.pause_start_time: float = 0.0

        curses.curs_set(0)  # Hide default cursor
        self.__init_color_pairs()

    def set_player(self, player: Player) -> None:
        """
        Sets the current player.

        Parameters:
            player (Player): The player to set as the current player.
        """

        self.player = player

    def draw(self) -> None:
        """
        Draws the entire game interface, including the game board, cursor, player information, controls, and high scores.
        """

        self.__draw_grid()
        self.__draw_cursor()
        self.__draw_info_and_status()
        self.__draw_controls()
        self.__draw_highscores()

    def __init_color_pairs(self) -> None:
        """
        Initializes color pairs for the terminal display.

        This method checks if the terminal supports colors and initializes color pairs accordingly.
        """

        if not curses.has_colors():
            return

        curses.start_color()

        if curses.COLORS < 8:
            return

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)

    def __get_color_pair(self, x: int, y: int, num: int, board: Board) -> int:
        """
        Determines the color pair to use for a specific cell based on its position and value.

        Parameters:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            num (int): The number in the cell.
            board (Board): The game board.

        Returns:
            int: The color pair index.
        """

        base_color: int = 3 if (x // 3 + y // 3) % 2 == 0 else 2

        if board.grid[y][x] != 0 and board.grid[y][x] == board.reset_grid[y][x]:
            base_color = 5 if (x // 3 + y // 3) % 2 == 0 else 4

        if num == board.highlighted_number:
            base_color = 7 if (x // 3 + y // 3) % 2 == 0 else 6

        return base_color

    def draw_name_input(self) -> str:
        """
        Draws the name input prompt and returns the entered name.

        Returns:
            str: The name entered by the user.
        """

        _, max_x = self.stdscr.getmaxyx()

        curses.echo()

        prompt = "Please enter your name: "
        start_x: int = max_x // 2 - len(prompt) // 2
        self.stdscr.addstr(5, start_x, prompt)

        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(6, start_x + 10, " " * 10)
        self.stdscr.move(6, start_x + 10)
        self.stdscr.attroff(curses.color_pair(2))

        name = self.stdscr.getstr(6, start_x + 10).decode("utf-8")
        curses.noecho()
        self.stdscr.clear()
        self.stdscr.refresh()

        return name

    def __draw_cell(self, origin: Origin, cell: Cell) -> None:
        """
        Draws a single cell of the Sudoku board.

        Parameters:
            origin (Origin): The (y, x) offset at which the board starts.
            cell (Cell): Contains row, col, num, and color_pair for this cell.
        """
        # Leerzeichen für 0, sonst die Zahl
        num_str = str(cell.num) if cell.num != 0 else " "

        # Absolute Position auf dem Bildschirm
        y = origin.y + cell.row
        x = origin.x + cell.col * 2

        # Zeichnen mit Farbe und Fettdruck
        self.stdscr.addstr(
            y, x, num_str, curses.color_pair(cell.color_pair) | curses.A_BOLD
        )

    def __draw_grid(self) -> None:
        """
        Draws the Sudoku game grid.

        This method iterates over the board and draws each cell using the appropriate color pair.
        """

        max_y, max_x = self.stdscr.getmaxyx()
        start_y: int = max_y // 2 - len(self.board.grid) // 2
        start_x: int = max_x // 2 - (len(self.board.grid[0]) * 2) // 2

        for y, row in enumerate(self.board.grid):
            for x, num in enumerate(row):
                color_pair = self.__get_color_pair(x, y, num, self.board)
                origin = Origin(start_y, start_x)
                cell = Cell(y, x, num, color_pair)
                self.__draw_cell(origin, cell)

    def draw_start_game(self) -> None:
        """
        Displays a start game message in the center of the screen, inviting
        the user to press any key to begin playing.
        """

        _, max_x = self.stdscr.getmaxyx()

        text: str = "Press any key to start the game"

        start_x: int = max_x // 2 - len(text) // 2

        self.stdscr.addstr(5, start_x, text, curses.color_pair(7))

    def draw_clock(self) -> None:
        """
        Continuously displays an elapsed time clock at the top center of the screen.

        Starts the timer when called and updates the displayed time every second.
        Handles pausing the timer when `self.timer_paused` is True.
        """

        _, max_x = self.stdscr.getmaxyx()

        self.start_time = time.time()

        while True:
            if self.timer_paused:
                elapsed_time = int(self.pause_start_time - self.start_time)
            else:
                elapsed_time = int(time.time() - self.start_time)

            self.board.time = elapsed_time
            self.player.score = elapsed_time

            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_str: str = f"Elapsed time: {hours:02}:{minutes:02}:{seconds:02}"

            start_x: int = max_x // 2 - len(time_str) // 2

            self.stdscr.addstr(3, start_x, time_str)
            self.stdscr.refresh()

            time.sleep(1)

    def __draw_info_and_status(self) -> None:
        """
        Draws the title, subtitle, and a status bar at the bottom of the screen.

        The status bar shows information about the current cursor position, selected number,
        pressed key, highlighted number, difficulty, and player name.
        """

        max_y, max_x = self.stdscr.getmaxyx()

        title: str = "Sudoku"[: max_x - 1]
        start_x_title: int = max_x // 2 - len(title) // 2
        self.stdscr.addstr(1, start_x_title, title, curses.A_BOLD)

        subtitle: str = "Written by Julian Hoffmann"[: max_x - 1]
        start_x_subtitle: int = max_x // 2 - len(subtitle) // 2
        self.stdscr.addstr(2, start_x_subtitle, subtitle)

        status_text: str = (
            f" Pos: ({self.board.cursor.x}, {self.board.cursor.y}) |"
            f" Num: ({self.board.grid[self.board.cursor.y, self.board.cursor.x]}) |"
            f" Pressed key: {chr(self.board.current_key)}({self.board.current_key}) |"
            f" Highlighted num: {str(self.board.highlighted_number)} |"
            f" Difficulty: {str(self.board.difficulty)} |"
            f" Name: {(self.player.name if self.player is not None else '')}"
        )[: max_x - 1]
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(max_y - 1, 0, status_text)
        self.stdscr.addstr(
            max_y - 1, len(status_text), " " * (max_x - len(status_text) - 1)
        )
        self.stdscr.attroff(curses.color_pair(1))

    def __draw_controls(self) -> None:
        """
        Draws a control panel with game instructions on the right side of the screen.

        The panel lists available keys and their functions in the game, such as navigation,
        number input, saving/loading, etc.
        """

        max_y, max_x = self.stdscr.getmaxyx()
        panel_width: int = 27
        start_x: int = max_x - panel_width

        self.stdscr.vline(0, start_x - 1, "|", max_y - 1)

        controls: list[str] = [
            "Controls:",
            "Arrow keys: Navigate",
            "'q': Quit Sudoku",
            "'r': Reset board",
            "'c': Check solution",
            "'0-9': Number input",
            "'+': Incr. highlighted num",
            "'-': Decr. highlighted num",
            "'s': Save game state",
            "'l': Load game state",
            "'a': Start AI solver",
        ]

        for i, text in enumerate(controls):
            self.stdscr.addstr(i + 1, start_x, text[: panel_width - 1])

    def __draw_highscores(self) -> None:
        """
        Displays a list of high scores on the left side of the screen.

        The high scores are filtered by difficulty and show the name and time of the top 15 players for the current difficulty level.
        """

        max_y, _ = self.stdscr.getmaxyx()
        panel_width: int = 27
        start_x: int = 0

        self.stdscr.vline(0, panel_width - 1, "|", max_y - 1)

        highscores = self.hs_manager.highscores

        title: str = f"{highscores['title']} (Top 15):"
        top10_len: int = len("(Top 15)")
        self.stdscr.addstr(1, start_x, title[: panel_width - 1])
        self.stdscr.addstr(2, start_x, "name:"[: panel_width - 1])
        self.stdscr.addstr(
            2, start_x + len(title) - top10_len, "score (s):"[: panel_width - 1]
        )

        filtered_highscores = [
            item
            for item in highscores["scores"][:15]
            if item["difficulty"] == str(self.board.difficulty)
        ]
        for i, item in enumerate(filtered_highscores):
            name: str = StringUtil.shorten_string(item["name"], max_length=10)
            score: str = str(item["score"])
            self.stdscr.addstr(i + 3, start_x, name)
            self.stdscr.addstr(
                i + 3, start_x + len(title) - top10_len, score[: panel_width - 1]
            )

    def __draw_cursor(self) -> None:
        """
        Draws a cursor highlighting the currently selected cell on the Sudoku board.

        The cursor's appearance (bold and color) depends on the cell's background color.
        """

        max_y, max_x = self.stdscr.getmaxyx()
        start_y: int = max_y // 2 - len(self.board.grid) // 2
        start_x: int = max_x // 2 - (len(self.board.grid[0]) * 2) // 2

        num: int = self.board.grid[self.board.cursor.y][self.board.cursor.x]
        num_str: str = str(num) if num != 0 else " "

        cell_color_pair: int = (
            2 if (self.board.cursor.x // 3 + self.board.cursor.y // 3) % 2 == 0 else 1
        )

        if cell_color_pair != 2:
            cursor_attr: int = curses.color_pair(3) | curses.A_BOLD
        else:
            cursor_attr: int = curses.color_pair(2) | curses.A_BOLD

        self.stdscr.addstr(
            start_y + self.board.cursor.y,
            start_x + self.board.cursor.x * 2,
            num_str,
            cursor_attr,
        )

    def draw_ai_player_notice(self) -> None:
        """
        Displays a notice that the AI player is currently solving the puzzle.
        """

        _, max_x = self.stdscr.getmaxyx()

        text: str = "AiPlayer is solving the puzzle for you!"

        start_x: int = max_x // 2 - len(text) // 2

        self.stdscr.addstr(5, start_x, text, curses.color_pair(7))
        self.stdscr.refresh()

    def draw_game_over(self, score: int) -> None:
        """
        Displays a game over screen when the puzzle is solved correctly.

        Shows congratulatory messages and the time taken to solve the puzzle.
        Waits for any key press before clearing the screen.

        Args:
            score (int): The time taken to solve the puzzle.
        """

        self.stdscr.clear()

        height, width = self.stdscr.getmaxyx()

        text: str = "Congratulations!"
        start_y: int = height // 2
        start_x: int = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        text = "Your solution was correct!"
        start_y += 2
        start_x = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        text = f"You took {score} seconds to finish the puzzle."
        start_y += 2
        start_x = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        text = "Press any key to exit."
        start_y += 2
        start_x = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        self.stdscr.getch()
        self.stdscr.clear()

    def draw_game_continue(self, score: int) -> None:
        """
        Displays a message to continue the game if the solution is incorrect.

        Shows the current time and prompts the user to press any key to continue playing.
        """

        self.stdscr.clear()

        height, width = self.stdscr.getmaxyx()

        text: str = "Your solution is not correct."
        start_y: int = height // 2
        start_x: int = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        text = "Keep on going!"
        start_y += 2
        start_x = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        text = f"Current time: {score}"
        start_y += 2
        start_x = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        text = "Press any key to continue."
        start_y += 2
        start_x = width // 2 - len(text) // 2
        self.stdscr.addstr(start_y, start_x, text)

        self.stdscr.getch()
        self.stdscr.clear()
        self.stdscr.refresh()
