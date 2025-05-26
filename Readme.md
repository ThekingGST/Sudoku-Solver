# 🧩 Sudoku Solver

This is a simple, terminal-based **Sudoku solving and interaction tool** written in Python. It allows users to manually input values into a Sudoku board, validates each entry according to Sudoku rules, and includes an automatic logic-based solving helper. It’s perfect for learning, practicing, or demonstrating Sudoku logic in real time.



## 🖼️ Application Preview




## ⚙️ How it works

The application:

1. **Displays the Sudoku board** in a grid layout using special characters to represent empty cells (`☒`).
2. **Accepts user input** for filling cells, checks if the number is valid in its row, column, and 3×3 box.
3. Provides **reasoning** for invalid entries.
4. **Validates the final board** to ensure it's solved correctly.
5. If the board isn’t complete, it uses a **basic logic solver** to fill in cells that have only one possible valid number.



## 🧑‍💻 How to Use

1. **Run the script** in a terminal using Python 3.
2. On launch, it displays the current Sudoku puzzle.
3. You'll be prompted to enter:

   * A **row number** (1–9),
   * A **column number** (1–9),
   * A **number** to place (1–9).
4. The program checks your move and lets you know if it’s valid.
5. Type `'q'` at any time to stop entering values.
6. Once you exit input mode, the app will check if the puzzle is solved.

   * If not, it will attempt to solve using logic and display the result.



## 🧾 Version List

* **v1**: First Version
  * ✅ Terminal-based Sudoku game interface with grid and Unicode symbols
  * ✅ Real-time entry validation with helpful error messages
  * ✅ Basic logical solver to complete the board when user input ends
  * ✅ Final board validation and feedback with success/failure message

---
