import sys

def print_board(board):
    for r, row in enumerate(board):
        print('row %3d: %s'%(r, row))
    print('')

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
        if i + 1 in [6, 64]:
            count = sum([1 for row in board for v in row if v == 'O'])
            print('after {} steps {} plots are reachable'.format(i + 1, count))

    board = [[c for c in line.strip()] for line in lines]
    num_rows = len(board)
    num_cols = len(board[0])

    start_coord = (-999, -999)
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == 'S':
                start_coord = (r, c)
                board[r][c] = '.'

    print('start coord is {}'.format(start_coord))

    work_list_back2 = set()
    count_back2 = 0
    work_list_back1 = set([start_coord])
    count_back1 = 1
    count = 0
    for i in range(5000):
        work_list = set()
        for r, c in work_list_back1:
            if (board[(r-1) % num_rows][c % num_cols] == '.'): # and
                #not (r-1, c) in work_list_back2):
                work_list.add((r-1, c))
            if (board[(r+1) % num_rows][c % num_cols] == '.'): # and
                #not (r+1, c) in work_list_back2):
                work_list.add((r+1, c))
            if (board[r % num_rows][(c-1) % num_cols] == '.'): # and
                #not (r, c-1) in work_list_back2):
                work_list.add((r, c-1))
            if (board[r % num_rows][(c+1) % num_cols] == '.'): # and
                #not (r, c+1) in work_list_back2):
                work_list.add((r, c+1))
        work_list = work_list.difference(work_list_back2)
        work_list_back2 = work_list_back1
        work_list_back1 = work_list

        count = len(work_list) + count_back2
        count_back2 = count_back1
        count_back1 = count
        #print('on step {} there are {} items on the work list'.format(i + 1, len(work_list)))
        #print('    work_list is {}'.format(work_list))
        if i + 1 in [6, 10, 50, 100, 500, 1000, 5000]:
            print('after {} steps {} plots are reachable'.format(i + 1, count))
            print('   there are currently {} items on the work list'.format(len(work_list)))
