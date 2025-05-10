# SudokuPy
[![tests](https://github.com/itacentury/SudokuPy/actions/workflows/python-test.yml/badge.svg)](https://github.com/itacentury/SudokuPy/actions/workflows/python-test.yml)

## Instructions

### Setup

1. Install Python 3.10.0 or newer
2. Create and open new `virtual environment`
3. Install required modules with `pip install -r requirements.txt`
4. Run project with `python main.py`

### Configuration

* There are 3 possible difficulties:
  * Easy
  * Medium
  * Hard
* Running `python main.py` will generate a Sudoku board with `medium` difficulty by default.
* To change the difficulty, enter the desired difficulty after `main.py`
* For example: `python main.py easy` or `python main.py hard`

### Layout

* On the left the top 15 high scores with your chosen difficulty will be shown.
* On the right the controls are shown.
  * Navigating through the Sudoku grid is done using the arrow keys.
  * Ending and quitting the current game is done by pressing `q`. FYI: There is no confirmation question or window.
  * To completely reset the board to the initial state, use the `r` key.
  * To check if your filled out board is correct, press `c`. If your solution is correct, your high score will be saved, and the game will exit.
  * To input numbers into the board, use the number keys `0-9`. Use `0` to delete the currently entered number.
  * To increase or decrease the currently highlighted number use `+` and `-`.
  * If you have to quit playing due to unforeseen circumstances, you can save the state with `s`. To reload your saved game, use `l`.
  * If the current board is too hard for you, you can try to let an AI solve it for you. Use the `a` key to let the AI do its thing.
* At the bottom there are several debug information which might be useful or interesting for you.

### Playing

1. Start the game with `python main.py`
2. Enter your name as the instructions on the screen says. This is needed for your score to be saved and be connected to you. Press enter to save your name.
3. You now have time to look at the generated sudoku board until you press any key. During that time you can make yourself familiar with the layout.
4. After pressing a key the game starts and so does the timer!
5. If you are done playing press `c` to check if your solution is correct.

### Tests

Tested with following operating systems:

* Windows 11
* Linux Debian bookworm
