
def check_win(board):
    EMPTY = 0
    ROWS = len(board)
    COLS = len(board[0])

    def line_winner(line):
        for i in range(len(line) - 3):
            if line[i] != EMPTY and all(line[i + j] == line[i] for j in range(4)):
                return line[i]
        return None

    # Rows
    for row in board:
        winner = line_winner(row)
        if winner:
            return winner

    # Columns
    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        winner = line_winner(col)
        if winner:
            return winner

    # Diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] != EMPTY and all(board[r+i][c+i] == board[r][c] for i in range(4)):
                return board[r][c]
        for c in range(3, COLS):
            if board[r][c] != EMPTY and all(board[r+i][c-i] == board[r][c] for i in range(4)):
                return board[r][c]

    return None
