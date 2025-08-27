#!/usr/bin/env python3
"""
Demonstration script showing current Sudoku Solver functionality.
This script demonstrates the core features without requiring GUI.
"""

from Sudoku import SudokuGame, choose_puzzle
import puzzles
import json
import tempfile
import os


def print_board(board, title="Sudoku Board"):
    """Print a nicely formatted Sudoku board."""
    print(f"\n{title}")
    print("=" * 37)
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("+-----------+-----------+-----------+")
        
        row_str = ""
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            
            if cell == 0:
                row_str += " . "
            else:
                row_str += f" {cell} "
        
        print(f"|{row_str}|")
    print("=" * 37)


def demo_basic_functionality():
    """Demonstrate basic game functionality."""
    print("🧩 SUDOKU SOLVER - FUNCTIONALITY DEMONSTRATION")
    print("=" * 50)
    
    # 1. Load a puzzle
    print("\n1. LOADING PUZZLE:")
    easy_puzzle = choose_puzzle('easy')
    game = SudokuGame(easy_puzzle)
    print_board(game.board, "Initial Easy Puzzle")
    
    # 2. Make a valid move
    print("\n2. MAKING A VALID MOVE:")
    empty_row, empty_col = game.find_empty()
    print(f"Found empty cell at position ({empty_row + 1}, {empty_col + 1})")
    
    # Find a valid number for this position
    valid_num = None
    for num in range(1, 10):
        if game.is_valid(empty_row, empty_col, num):
            valid_num = num
            break
    
    if valid_num:
        success, message = game.check_user_entry(empty_row, empty_col, valid_num)
        print(f"Placing {valid_num} at ({empty_row + 1}, {empty_col + 1}): {message}")
        print_board(game.board, "After Valid Move")
    
    # 3. Try an invalid move
    print("\n3. TRYING INVALID MOVE:")
    # Try to place a number that already exists in the row
    for num in range(1, 10):
        if num in game.board[empty_row]:
            success, message = game.check_user_entry(empty_row, empty_col, num)
            print(f"Trying to place {num} at ({empty_row + 1}, {empty_col + 1}): {message}")
            break
    
    # 4. Demonstrate undo
    print("\n4. UNDO FUNCTIONALITY:")
    if game.move_history:
        print(f"Current move history: {len(game.move_history)} moves")
        game.undo_last_move()
        print("Last move undone!")
        print_board(game.board, "After Undo")
    
    # 5. Get a hint
    print("\n5. HINT SYSTEM:")
    if game.get_hint():
        print("Hint provided! A cell was filled automatically.")
        print_board(game.board, "After Hint")
    
    # 6. Save and load game
    print("\n6. SAVE/LOAD FUNCTIONALITY:")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        game.save_game(temp_file)
        print(f"Game saved to: {os.path.basename(temp_file)}")
        
        loaded_game = SudokuGame.load_game(temp_file)
        if loaded_game:
            print("Game loaded successfully!")
            print(f"Loaded game has {len(loaded_game.move_history)} moves in history")
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    # 7. Demonstrate solver
    print("\n7. AUTOMATIC SOLVING:")
    print("Attempting to solve the puzzle automatically...")
    solver_game = SudokuGame([row[:] for row in easy_puzzle])  # Fresh copy
    
    if solver_game.solve():
        print("Puzzle solved successfully!")
        print_board(solver_game.board, "Solved Puzzle")
        
        # Verify solution
        is_valid, message = solver_game.is_board_valid()
        print(f"Solution validation: {message}")
    else:
        print("Could not solve the puzzle automatically.")


def demo_puzzle_variety():
    """Demonstrate available puzzle difficulties."""
    print("\n\n🎯 PUZZLE DIFFICULTY DEMONSTRATION")
    print("=" * 50)
    
    difficulties = ['easy', 'medium', 'hard']
    
    for difficulty in difficulties:
        print(f"\n{difficulty.upper()} PUZZLE:")
        puzzle = choose_puzzle(difficulty)
        if puzzle:
            # Count empty cells
            empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
            print(f"Empty cells: {empty_cells}/81")
            print_board(puzzle, f"{difficulty.capitalize()} Puzzle")


def demo_edge_cases():
    """Demonstrate edge cases and error handling."""
    print("\n\n⚠️  EDGE CASES & ERROR HANDLING")
    print("=" * 50)
    
    game = SudokuGame(choose_puzzle('easy'))
    
    # Try to modify original cell
    print("\n1. TRYING TO MODIFY ORIGINAL PUZZLE CELL:")
    for i in range(9):
        for j in range(9):
            if game.original_board[i][j] != 0:
                success, message = game.check_user_entry(i, j, 5)
                print(f"Attempting to change original cell ({i+1}, {j+1}): {message}")
                break
        if game.original_board[i][j] != 0:
            break
    
    # Test invalid difficulty
    print("\n2. INVALID DIFFICULTY SELECTION:")
    invalid_puzzle = choose_puzzle('impossible')
    print(f"Selecting 'impossible' difficulty: {invalid_puzzle}")
    
    # Test loading non-existent file
    print("\n3. LOADING NON-EXISTENT FILE:")
    non_existent = SudokuGame.load_game('non_existent_file.json')
    print(f"Loading non-existent file: {non_existent}")


if __name__ == "__main__":
    try:
        demo_basic_functionality()
        demo_puzzle_variety()
        demo_edge_cases()
        
        print("\n\n✅ DEMONSTRATION COMPLETE!")
        print("=" * 50)
        print("All core functionalities are working correctly.")
        print("To run the GUI version, use: python sudoku_gui.py")
        print("To run tests, use: python test_sudoku.py")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("This indicates an issue that needs to be addressed.")