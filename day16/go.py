import sys

def debug(str):
    #print(str)
    pass

def print_mirrors(mirrors):
    print('>>> Mirrors are:')
    for line in mirrors:
        print('{}'.format(line))
    print('<<< End of Mirrors.')

def is_valid(pos, mirrors):
    if pos[0] < 0: return False
    if pos[1] < 0: return False
    if pos[0] >= len(mirrors[0]): return False
    if pos[1] >= len(mirrors): return False
    return True

def get_value(pos, mirrors):
    return mirrors[pos[1]][pos[0]]

def new_pos(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])

def trace_path(pos, dir, mirrors, energized, visited):
    debug('checking location {}, direction {}...'.format(pos, dir))
    while is_valid(pos, mirrors) and not (pos, dir) in visited:
        energized.add(pos)
        visited.add((pos, dir))
        v = get_value(pos, mirrors)
        if (v == '.') or (v == '-' and dir[1] == 0) or (v == '|' and dir[0] == 0):
            debug('tile is {}, continuing along same path.'.format(v))
            pos = new_pos(pos, dir)
            continue
        if v == '-':
            debug('tile is {}, splitting horizontally.'.format(v))
            dir0 = (1, 0)
            dir1 = (-1, 0)
            trace_path(new_pos(pos, dir0), dir0, mirrors, energized, visited)
            trace_path(new_pos(pos, dir1), dir1, mirrors, energized, visited)
            return
        if v == '|':
            debug('tile is {}, splitting vertically.'.format(v))
            dir0 = (0, 1)
            dir1 = (0, -1)
            trace_path(new_pos(pos, dir0), dir0, mirrors, energized, visited)
            trace_path(new_pos(pos, dir1), dir1, mirrors, energized, visited)
            return
        if v == '/':
            debug('tile is {}, bending.'.format(v))
            dir = (-dir[1], -dir[0])
            pos = new_pos(pos, dir)
            continue
        if v == '\\':
            debug('tile is {}, bending.'.format(v))
            dir = (dir[1], dir[0])
            pos = new_pos(pos, dir)
            continue

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    mirrors = [line.strip() for line in lines]

    energized = set()
    trace_path((0, 0), (1, 0), mirrors, energized, set())

    print('after tracing mirrors {} tiles are energized'.format(len(energized)))

    count = 0

    right = len(mirrors[0]) - 1
    bottom = len(mirrors) - 1
    for row in range(len(mirrors)):
        energized = set()
        trace_path((0, row), (1, 0), mirrors, energized, set())       # left edge
        if len(energized) > count: count = len(energized)

        energized = set()
        trace_path((right, row), (-1, 0), mirrors, energized, set())  # right edge
        if len(energized) > count: count = len(energized)

    for col in range(len(mirrors[0])):
        energized = set()
        trace_path((col, 0), (0, 1), mirrors, energized, set())       # top edge
        if len(energized) > count: count = len(energized)

        energized = set()
        trace_path((col, bottom), (0, -1), mirrors, energized, set())  # bottom edge
        if len(energized) > count: count = len(energized)

    print('maximum number of lit tiles is {}'.format(count))
