"""
Basic tests for Sudoku Solver functionality.
This demonstrates what testing infrastructure could look like.
"""

import unittest
import json
import os
import tempfile
from Sudoku import SudokuGame, choose_puzzle
import puzzles


class TestSudokuGame(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.easy_puzzle = puzzles.EASY_PUZZLES[0]
        self.game = SudokuGame(self.easy_puzzle)
    
    def test_game_initialization(self):
        """Test that game initializes correctly."""
        self.assertIsNotNone(self.game.board)
        self.assertEqual(len(self.game.board), 9)
        self.assertEqual(len(self.game.board[0]), 9)
        self.assertEqual(self.game.original_board, self.easy_puzzle)
        self.assertEqual(len(self.game.move_history), 0)
    
    def test_valid_move(self):
        """Test that valid moves are accepted."""
        # Find an empty cell
        empty_row, empty_col = self.game.find_empty()
        
        # Try a valid number
        for num in range(1, 10):
            if self.game.is_valid(empty_row, empty_col, num):
                valid, message = self.game.check_user_entry(empty_row, empty_col, num)
                self.assertTrue(valid)
                self.assertEqual(message, "Valid move!")
                self.assertEqual(self.game.board[empty_row][empty_col], num)
                break
    
    def test_invalid_move_original_cell(self):
        """Test that original puzzle cells cannot be modified."""
        # Find a cell with original number
        for i in range(9):
            for j in range(9):
                if self.game.original_board[i][j] != 0:
                    valid, message = self.game.check_user_entry(i, j, 5)
                    self.assertFalse(valid)
                    self.assertEqual(message, "Cannot change the original puzzle numbers.")
                    return
    
    def test_invalid_move_row_conflict(self):
        """Test that moves creating row conflicts are rejected."""
        # Find an empty cell and a number that already exists in that row
        for i in range(9):
            for j in range(9):
                if self.game.board[i][j] == 0:
                    for num in range(1, 10):
                        if num in self.game.board[i]:
                            valid, message = self.game.check_user_entry(i, j, num)
                            self.assertFalse(valid)
                            self.assertIn("already exists in row", message)
                            return
    
    def test_save_and_load_game(self):
        """Test that game state can be saved and loaded."""
        # Make a move first
        empty_row, empty_col = self.game.find_empty()
        for num in range(1, 10):
            if self.game.is_valid(empty_row, empty_col, num):
                self.game.check_user_entry(empty_row, empty_col, num)
                break
        
        # Save game to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.game.save_game(temp_file)
            
            # Load game
            loaded_game = SudokuGame.load_game(temp_file)
            
            self.assertIsNotNone(loaded_game)
            self.assertEqual(loaded_game.board, self.game.board)
            self.assertEqual(loaded_game.original_board, self.game.original_board)
            self.assertEqual(loaded_game.move_history, self.game.move_history)
        
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_undo_functionality(self):
        """Test that moves can be undone."""
        initial_board = [row[:] for row in self.game.board]  # Deep copy
        
        # Make a move
        empty_row, empty_col = self.game.find_empty()
        for num in range(1, 10):
            if self.game.is_valid(empty_row, empty_col, num):
                self.game.check_user_entry(empty_row, empty_col, num)
                break
        
        # Verify move was made
        self.assertNotEqual(self.game.board, initial_board)
        self.assertEqual(len(self.game.move_history), 1)
        
        # Undo move
        result = self.game.undo_last_move()
        self.assertTrue(result)
        self.assertEqual(self.game.board, initial_board)
        self.assertEqual(len(self.game.move_history), 0)
    
    def test_hint_functionality(self):
        """Test that hint system works."""
        initial_empty_cells = sum(1 for i in range(9) for j in range(9) if self.game.board[i][j] == 0)
        
        # Get a hint
        result = self.game.get_hint()
        
        if result:  # Hint was provided
            final_empty_cells = sum(1 for i in range(9) for j in range(9) if self.game.board[i][j] == 0)
            self.assertEqual(final_empty_cells, initial_empty_cells - 1)
            self.assertEqual(len(self.game.move_history), 1)
            self.assertEqual(self.game.move_history[0][0], 'hint')
    
    def test_find_empty(self):
        """Test that find_empty correctly identifies empty cells."""
        empty_cell = self.game.find_empty()
        
        if empty_cell:
            row, col = empty_cell
            self.assertEqual(self.game.board[row][col], 0)
        else:
            # Board is full
            for i in range(9):
                for j in range(9):
                    self.assertNotEqual(self.game.board[i][j], 0)


class TestPuzzleSelection(unittest.TestCase):
    
    def test_choose_puzzle_easy(self):
        """Test that easy puzzle selection works."""
        puzzle = choose_puzzle('easy')
        self.assertIsNotNone(puzzle)
        self.assertIn(puzzle, puzzles.EASY_PUZZLES)
    
    def test_choose_puzzle_medium(self):
        """Test that medium puzzle selection works."""
        puzzle = choose_puzzle('medium')
        self.assertIsNotNone(puzzle)
        self.assertIn(puzzle, puzzles.MEDIUM_PUZZLES)
    
    def test_choose_puzzle_hard(self):
        """Test that hard puzzle selection works."""
        puzzle = choose_puzzle('hard')
        self.assertIsNotNone(puzzle)
        self.assertIn(puzzle, puzzles.HARD_PUZZLES)
    
    def test_choose_puzzle_invalid(self):
        """Test that invalid difficulty returns None."""
        puzzle = choose_puzzle('invalid')
        self.assertIsNone(puzzle)


class TestSudokuValidation(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = SudokuGame(puzzles.EASY_PUZZLES[0])
    
    def test_is_valid_empty_cell(self):
        """Test validation on empty cells."""
        empty_row, empty_col = self.game.find_empty()
        
        # Test valid number
        for num in range(1, 10):
            if self.game.is_valid(empty_row, empty_col, num):
                self.assertTrue(self.game.is_valid(empty_row, empty_col, num))
                break
    
    def test_puzzle_data_integrity(self):
        """Test that puzzle data is valid."""
        for difficulty, puzzles_list in [
            ('easy', puzzles.EASY_PUZZLES),
            ('medium', puzzles.MEDIUM_PUZZLES),
            ('hard', puzzles.HARD_PUZZLES)
        ]:
            for puzzle in puzzles_list:
                self.assertEqual(len(puzzle), 9, f"Puzzle in {difficulty} has wrong number of rows")
                for row in puzzle:
                    self.assertEqual(len(row), 9, f"Row in {difficulty} puzzle has wrong length")
                    for cell in row:
                        self.assertIn(cell, range(0, 10), f"Invalid cell value in {difficulty} puzzle")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)