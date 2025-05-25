# Print the Sudoku board with grid lines and symbols for empty cells
def print_board(board):
    print("■" + "▬" * 23 + "■")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("■" + "-" * 23 + "■")
        print("┃", end=" ")
        for j in range(9):
            cell = board[i][j]
            print(cell if cell != 0 else "☒", end=" ")
            if (j + 1) % 3 == 0 and j != 8:
                print("|", end=" ")
        print("┃")
    print("■" + "▬" * 23 + "■")

# Check if the user's entry is valid and give a reason if not
def check_user_entry(board, row, col, num):
    if board[row][col] != 0:
        return False, "Cell is already filled."
    if num in board[row]:
        return False, f"{num} already exists in row {row + 1}."
    if any(board[i][col] == num for i in range(9)):
        return False, f"{num} already exists in column {col + 1}."
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False, f"{num} already exists in the 3x3 box."
    return True, "Valid move!"

# Loop to allow user to enter numbers and check validity
def user_entry_loop(board):
    while True:
        print_board(board)
        choice = input("\nEnter 'q' to quit or press Enter to continue: ").strip().lower()
        if choice == 'q':
            print("Exiting input mode\n")
            break

        try:
            row = int(input("Enter row (1-9): ")) - 1
            col = int(input("Enter column (1-9): ")) - 1
            num = int(input("Enter number (1-9): "))

            if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                print("Invalid range. Try again.")
                continue

            valid, reason = check_user_entry(board, row, col, num)
            if valid:
                board[row][col] = num
                print(f"✅ Placed {num} at ({row + 1}, {col + 1}).\n")
            else:
                print(f"❌ Can't place here: {reason}\n")

        except ValueError:
            print("Invalid input. Please enter numbers only.\n")

# Check if a number can be placed at (row, col) without breaking Sudoku rules
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

# Return a list of valid numbers for a given cell
def get_possible_values(board, row, col):
    valid_numbers = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            valid_numbers.append(num)
    return valid_numbers

# Solve the Sudoku using simple logic (filling cells with only one possible value)
def solve_with_logic(board):
    changed = True
    while changed:
        changed = False
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    poss = get_possible_values(board, row, col)
                    if len(poss) == 1:
                        board[row][col] = poss[0]
                        changed = True
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

# Check if the board is completely and correctly filled
def is_board_valid(board):
    # Check for empty cells
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False, f"Cell ({row + 1}, {col + 1}) is empty."
                
    # Check rows
    for row in board:
        if sorted(row) != list(range(1, 10)):
            return False, f"An Invalid row found at {row+1}."

    # Check columns
    for col in range(9):
        column = [board[row][col] for row in range(9)]
        if sorted(column) != list(range(1, 10)):
            return False, f"An Invalid column {col + 1}."

    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(board[box_row + i][box_col + j])
            if sorted(box) != list(range(1, 10)):
                return False, f"Invalid 3×3 box starting at ({box_row + 1}, {box_col + 1})."

    return True, "Congrats!! You solved the Sudoku🎉🎉🎉!"

# Example board
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("»------• Welcome to Solving sudoku with ME! •------«")
print("\n\t🧩 Here's Your Sudoku Puzzle 🧩\n")
user_entry_loop(board)

is_valid_final, message = is_board_valid(board)
if is_valid_final:
    print(f"✅ {message}")
    print_board(board)
else:
    print(f"❌ Oops!! You made a mistake: {message}")
    solve_with_logic(board)
    print("Here's the solution:")
    print_board(board)

