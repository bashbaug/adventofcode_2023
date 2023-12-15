import sys
import copy

def print_board(board, label=''):
    print('==={}====================================================='.format(label))
    for line in board:
        print(line.strip())

def iterate_up(board):
    changed = False
    for row in range(1, len(board)):
        prev = board[row - 1]
        curr = board[row]
        for c in range(len(curr)):
            if curr[c] == 'O' and prev[c] == '.':
                prev = prev[:c] + 'O' + prev[c+1:]
                curr = curr[:c] + '.' + curr[c+1:]
                changed = True
        board[row - 1] = prev
        board[row] = curr
    return changed

def iterate_down(board):
    changed = False
    for row in range(len(board) - 1):
        curr = board[row]
        next = board[row + 1]
        for c in range(len(curr)):
            if curr[c] == 'O' and next[c] == '.':
                next = next[:c] + 'O' + next[c+1:]
                curr = curr[:c] + '.' + curr[c+1:]
                changed = True
        board[row] = curr
        board[row + 1] = next
    return changed

def iterate_left(board):
    changed = False
    for row, line in enumerate(board):
        for c in range(1, len(line)):
            if line[c] == 'O' and line[c-1] == '.':
                line = line[:c-1] + 'O' + '.' + line[c+1:]
                changed = True
        board[row] = line
    return changed

def iterate_right(board):
    changed = False
    for row, line in enumerate(board):
        for c in range(len(line) - 1):
            if line[c] == 'O' and line[c+1] == '.':
                line = line[:c] + '.' + 'O' + line[c+2:]
                changed = True
        board[row] = line
    return changed

def iterate_spin(board):
    while iterate_up(board): pass
    while iterate_left(board): pass
    while iterate_down(board): pass
    while iterate_right(board): pass

def compute_load(board):
    total_load = 0
    for row, line in enumerate(board):
        load = len(board) - row
        for c in line:
            if c == 'O':
                total_load = total_load + load
    return total_load

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    board = copy.deepcopy(lines)
    while iterate_up(board): pass

    total_load = compute_load(board)
    print('total load for part one is: {}'.format(total_load))

    board = copy.deepcopy(lines)
    for i in range(1000000000):
        iterate_spin(board)
        total_load = compute_load(board)
        print('total load after iteration {} is {}'.format(i + 1, total_load))

    # Find the cycle.
    # Compute 1000000000 % cycle length.
    # Find an iteration with the same number --> this is the answer.
