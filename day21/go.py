import sys

def reset_board(board):
    return [['#' if c == '#' else '.' for c in row] for row in board]

def iterate_board(board):
    next_board = reset_board(board)
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == 'O':
                if r > 0:
                    if next_board[r-1][c] == '.': next_board[r-1][c] = 'O'
                if r < len(board) - 1:
                    if next_board[r+1][c] == '.': next_board[r+1][c] = 'O'
                if c > 0:
                    if next_board[r][c-1] == '.': next_board[r][c-1] = 'O'
                if c < len(row) - 1:
                    if next_board[r][c+1] == '.': next_board[r][c+1] = 'O'
    return next_board

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    board = [[c if c != 'S' else 'O' for c in line.strip()] for line in lines]
    for i in range(64):
        board = iterate_board(board)

    count = sum([1 for row in board for v in row if v == 'O'])
    print('{} plots are reachable'.format(count))
