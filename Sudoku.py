import copy
import random
import puzzles
import json
import os

class SudokuGame:
    def __init__(self, board):
        self.board = board
        self.original_board = copy.deepcopy(board)
        self.move_history = []

    def check_user_entry(self, row, col, num):
        if self.original_board[row][col] != 0:
            return False, "Cannot change the original puzzle numbers."
        if num in self.board[row]:
            return False, f"{num} already exists in row {row + 1}."
        if any(self.board[i][col] == num for i in range(9)):
            return False, f"{num} already exists in column {col + 1}."
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False, f"{num} already exists in the 3x3 box."

        self.board[row][col] = num
        self.move_history.append(('user', row, col, num))
        return True, "Valid move!"

    def get_hint(self):
        empty_cell = self.find_empty()
        if not empty_cell:
            return False

        temp_game = SudokuGame(copy.deepcopy(self.board))
        if temp_game.solve():
            row, col = empty_cell
            hint_num = temp_game.board[row][col]
            self.board[row][col] = hint_num
            self.move_history.append(('hint', row, col, hint_num))
            return True
        return False

    def undo_last_move(self):
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        _, row, col, _ = last_move
        self.board[row][col] = 0
        return True

    def save_game(self, filename):
        game_state = {
            "board": self.board,
            "original_board": self.original_board,
            "move_history": self.move_history
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f)

    @staticmethod
    def load_game(filename):
        if not os.path.exists(filename):
            return None

        with open(filename, 'r') as f:
            game_state = json.load(f)

        game = SudokuGame(game_state['board'])
        game.original_board = game_state['original_board']
        game.move_history = game_state['move_history']
        return game

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num and i != col:
                return False
        for i in range(9):
            if self.board[i][col] == num and i != row:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num and (i, j) != (row, col):
                    return False
        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(row, col, i):
                self.board[row][col] = i
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

    def is_board_valid(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False, f"Cell ({row + 1}, {col + 1}) is empty."
        # ... (rest of the validation logic)
        return True, "Congrats!! You solved the Sudoku🎉🎉🎉!"

def choose_puzzle(difficulty):
    if difficulty == 'easy':
        return random.choice(puzzles.EASY_PUZZLES)
    elif difficulty == 'medium':
        return random.choice(puzzles.MEDIUM_PUZZLES)
    elif difficulty == 'hard':
        return random.choice(puzzles.HARD_PUZZLES)
    return None
