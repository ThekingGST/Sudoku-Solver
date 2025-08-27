import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from Sudoku import SudokuGame, choose_puzzle

class SudokuGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("550x650")

        self.game = None

        # Top frame for difficulty selection
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(pady=10)

        # Grid frame
        self.grid_frame = tk.Frame(self, bd=2, relief="solid")
        self.grid_frame.pack(pady=20)

        self.cells = {}
        self.create_grid()

        # Button frame
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.create_buttons()

        # Status bar
        self.status_bar = tk.Label(self, text="Welcome to Sudoku!", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.new_game()

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                # Add thicker lines for 3x3 boxes
                pad_x = (5, 0) if j % 3 == 0 and j != 0 else (1, 1)
                pad_y = (5, 0) if i % 3 == 0 and i != 0 else (1, 1)

                frame = tk.Frame(self.grid_frame)
                frame.grid(row=i, column=j, padx=pad_x, pady=pad_y)

                entry = tk.Entry(frame, width=2, font=('Arial', 20), justify='center', bd=1, relief="solid")
                entry.pack()
                self.cells[(i, j)] = entry
                entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.cell_input(e, r, c))

    def create_buttons(self):
        new_game_btn = tk.Button(self.button_frame, text="New Game", command=self.new_game)
        new_game_btn.pack(side="left", padx=5)

        save_btn = tk.Button(self.button_frame, text="Save Game", command=self.save_game)
        save_btn.pack(side="left", padx=5)

        load_btn = tk.Button(self.button_frame, text="Load Game", command=self.load_game)
        load_btn.pack(side="left", padx=5)

        hint_btn = tk.Button(self.button_frame, text="Hint", command=self.get_hint)
        hint_btn.pack(side="left", padx=5)

        undo_btn = tk.Button(self.button_frame, text="Undo", command=self.undo_move)
        undo_btn.pack(side="left", padx=5)

        solve_btn = tk.Button(self.button_frame, text="Solve", command=self.solve_puzzle)
        solve_btn.pack(side="left", padx=5)

    def new_game(self):
        difficulty = simpledialog.askstring("New Game", "Choose difficulty (easy, medium, hard):", parent=self)
        if difficulty and difficulty.lower() in ['easy', 'medium', 'hard']:
            board = choose_puzzle(difficulty.lower())
            self.game = SudokuGame(board)
            self.update_grid()
            self.status_bar.config(text=f"New {difficulty.capitalize()} game started.")
        else:
            self.status_bar.config(text="Invalid difficulty. Game not started.")

    def update_grid(self):
        if not self.game:
            return
        for i in range(9):
            for j in range(9):
                cell_entry = self.cells[(i, j)]
                cell_value = self.game.board[i][j]

                cell_entry.delete(0, tk.END)
                if cell_value != 0:
                    cell_entry.insert(0, str(cell_value))

                if self.game.original_board[i][j] != 0:
                    cell_entry.config(state='disabled', disabledbackground="#f0f0f0", disabledforeground="black")
                else:
                    cell_entry.config(state='normal', bg="white", fg="blue")

    def cell_input(self, event, row, col):
        entry = self.cells[(row, col)]
        value = entry.get()

        if value == "":
            self.game.board[row][col] = 0
            return

        if not value.isdigit() or not (1 <= int(value) <= 9):
            entry.delete(0, tk.END)
            self.status_bar.config(text="Invalid input. Please enter a number between 1 and 9.")
            return

        num = int(value)
        # Temporarily set to 0 to check validity correctly
        original_val = self.game.board[row][col]
        self.game.board[row][col] = 0

        valid, reason = self.game.check_user_entry(row, col, num)
        if valid:
            self.game.board[row][col] = num
            self.game.move_history.append(('user', row, col, num))
            self.status_bar.config(text=f"Placed {num} at ({row+1}, {col+1}).")
        else:
            self.game.board[row][col] = original_val # Restore original value
            entry.delete(0, tk.END)
            entry.insert(0, str(original_val) if original_val != 0 else "")
            self.status_bar.config(text=f"Error: {reason}")

        if self.check_win():
             self.status_bar.config(text="Congratulations! You solved the puzzle!")

    def get_hint(self):
        if self.game and self.game.get_hint():
            self.update_grid()
            self.status_bar.config(text="Hint provided.")
        else:
            self.status_bar.config(text="Could not provide a hint.")

    def undo_move(self):
        if self.game and self.game.undo_last_move():
            self.update_grid()
            self.status_bar.config(text="Last move undone.")
        else:
            self.status_bar.config(text="No moves to undo.")

    def solve_puzzle(self):
        if self.game and self.game.solve():
            self.update_grid()
            self.status_bar.config(text="Puzzle solved!")
        else:
            self.status_bar.config(text="Could not solve the puzzle.")

    def save_game(self):
        if not self.game:
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filepath:
            self.game.save_game(filepath)
            self.status_bar.config(text=f"Game saved to {os.path.basename(filepath)}")

    def load_game(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            self.game = SudokuGame.load_game(filepath)
            if self.game:
                self.update_grid()
                self.status_bar.config(text=f"Game loaded from {os.path.basename(filepath)}")
            else:
                self.status_bar.config(text="Failed to load game.")

    def check_win(self):
        for row in self.game.board:
            if 0 in row:
                return False

        is_valid, _ = self.game.is_board_valid()
        if is_valid:
            messagebox.showinfo("Sudoku", "Congratulations! You've solved the puzzle!")
            return True
        return False

if __name__ == "__main__":
    app = SudokuGUI()
    app.mainloop()
