import tkinter as tk
from tkinter import messagebox

# Constants
ROWS = 6
COLS = 7
DEPTH = 4

EMPTY = " "

# BoardManager Functions
def init_board():
    return [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
    ]

def current_player(board):
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return "X" if x_count <= o_count else "O"

def available_actions(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def take_action(board, action):
    new_board = [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
    ]

    for row in range(ROWS):
        for col in range(COLS):
            new_board[row][col] = board[row][col]

    player, column = action

    for r in range(ROWS - 1, -1, -1):
        if new_board[r][column] == EMPTY:
            new_board[r][column] = player
            break

    return new_board

def check_terminal(board):
    winner = check_win(board)
    if winner:
        return 1000 if winner == "O" else -1000
    elif not available_actions(board):
        return 0
    return "Not terminal"

def check_win(board):
    def line_winner(line):
        for i in range(len(line) - 3):
            if line[i] != EMPTY and all(line[i + j] == line[i] for j in range(4)):
                return line[i]
        return None

    
    for row in board:
        winner = line_winner(row)
        if winner:
            return winner

    
    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        winner = line_winner(col)
        if winner:
            return winner

    
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] != EMPTY and all(board[r+i][c+i] == board[r][c] for i in range(4)):
                return board[r][c]
        for c in range(3, COLS):
            if board[r][c] != EMPTY and all(board[r+i][c-i] == board[r][c] for i in range(4)):
                return board[r][c]

    return None

def evaluate_window(window, token):
    score = 0
    opponent = "X" if token == "O" else "O"

    if window.count(token) == 4:
        score += 1000
    elif window.count(token) == 3 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(token) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score

def evaluate_board(board, token):
    score = 0
    center_col = [board[r][COLS // 2] for r in range(ROWS)]
    score += center_col.count(token) * 6

    for row in board:
        for c in range(COLS - 3):
            window = row[c:c+4]
            score += evaluate_window(window, token)

    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col[r:r+4]
            score += evaluate_window(window, token)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, token)
        for c in range(3, COLS):
            window = [board[r+i][c-i] for i in range(4)]
            score += evaluate_window(window, token)

    return score

def alpha_beta(board, depth, alpha=float('-inf'), beta=float('inf')):
    result = check_terminal(board)

    if result != "Not terminal" or depth == 0:
        if result == "Not terminal":
            return evaluate_board(board, "O"), None
        return result, None

    player = current_player(board)
    best_action = None

    if player == "O":
        max_eval = float('-inf')
        for action in available_actions(board):
            next_state = take_action(board, ("O", action))
            eval, _ = alpha_beta(next_state, depth - 1, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_action = action
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_action

    else:
        min_eval = float('inf')
        for action in available_actions(board):
            next_state = take_action(board, ("X", action))
            eval, _ = alpha_beta(next_state, depth - 1, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_action

# GUI Functions
def setup_gui(root, drop_disc):
    circles = [[None for _ in range(COLS)] for _ in range(ROWS)]
    canvas_size = 70

    root.title("Connect 4 vs AI")
    root.geometry("600x550")

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    for c in range(COLS):
        btn = tk.Button(button_frame, text="↓", font=('Arial', 18), width=4, height=1,
                        command=lambda col=c: drop_disc(col))
        btn.grid(row=0, column=c, padx=5)

    board_frame = tk.Frame(root)
    board_frame.pack()

    for r in range(ROWS):
        for c in range(COLS):
            canvas = tk.Canvas(board_frame, width=canvas_size, height=canvas_size, bg="#4169e1", highlightthickness=0)
            canvas.grid(row=r, column=c, padx=2, pady=2)
            circle = canvas.create_oval(5, 5, canvas_size-5, canvas_size-5, fill="white", outline="#4169e1")
            circles[r][c] = (canvas, circle)

    return circles, canvas_size

def update_board(circles, board):
    for r in range(ROWS):
        for c in range(COLS):
            val = board[r][c]
            color = "white"
            if val == "X":
                color = "red"
            elif val == "O":
                color = "yellow"
            canvas, circle = circles[r][c]
            canvas.itemconfig(circle, fill=color)

def show_winner(root, winner):
    messagebox.showinfo("Game Over", f"{winner} wins!")
    root.quit()

# Game Logic
def start_game():
    root = tk.Tk()
    board = init_board()
    current_turn = "X"

    def drop_disc(col):
        nonlocal current_turn, board
        if current_turn == "X":
            if col in available_actions(board):
                board = take_action(board, ("X", col))
                update_board(circles, board)
                if check_win(board) == "X":
                    show_winner(root, "Player")
                else:
                    current_turn = "O"
                    root.after(300, ai_turn)

    def ai_turn():
        nonlocal current_turn, board
        _, action = alpha_beta(board, DEPTH)
        if action is not None:
            board = take_action(board, ("O", action))
            update_board(circles, board)
            if check_win(board) == "O":
                show_winner(root, "AI")
            else:
                current_turn = "X"

    circles, canvas_size = setup_gui(root, drop_disc)
    update_board(circles, board)

    root.mainloop()

if __name__ == "__main__":
    start_game()
