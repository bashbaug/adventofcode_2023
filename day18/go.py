import sys

OUTSIDE, TOP, INSIDE, BOTTOM = 0, 2, 1, 3

def evaluate_line(y, intervals):
    #print('evaluating line {}:'.format(y))
    count = 0
    state = OUTSIDE
    sx = 0
    for i in intervals:
        match_top = y == i[1]
        match_mid = i[1] < y and i[2] > y
        match_bot = y == i[2]
        #print('state is {}, sx is {}, count is {}, interval is {}, match_top is {}, match_mid is {}, match_bot is {}'.format(state, sx, count, i, match_top, match_mid, match_bot))
        if state == OUTSIDE:
            if match_top:
                sx = i[0]
                state = TOP
            if match_mid:
                sx = i[0]
                state = INSIDE
            if match_bot:
                sx = i[0]
                state = BOTTOM
        elif state == INSIDE:
            if match_top: state = BOTTOM
            if match_mid:
                count = count + i[0] - sx + 1
                state = OUTSIDE
            if match_bot: state = TOP
        elif state == BOTTOM:
            if match_top: state = INSIDE
            if match_mid: print('UNEXPECTED! matched middle from bottom.')
            if match_bot:
                count = count + i[0] - sx + 1
                state = OUTSIDE
        elif state == TOP:
            if match_top:
                count = count + i[0] - sx + 1
                state = OUTSIDE
            if match_mid: print('UNEXPECTED! matched middle from top.')
            if match_bot: state = INSIDE
    if state != OUTSIDE:
        print('UNEXPECTED!! ending state is {}'.format(state))
    return count

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    cx, cy = 0, 0
    intervals = []
    for line in lines:
        dir, dist, _ = line.split()
        dist = int(dist)
        if dir == 'R': cx = cx + dist
        if dir == 'L': cx = cx - dist
        if dir == 'D':
            ncy = cy + dist
            intervals.append((cx, cy, ncy))
            cy = ncy
        if dir == 'U':
            ncy = cy - dist
            intervals.append((cx, ncy, cy))
            cy = ncy

    intervals = sorted(intervals)
    miny = min([i[1] for i in intervals])
    maxy = max([i[2] for i in intervals])
    print('miny = {}, maxy = {}'.format(miny, maxy))

    count = 0
    for y in range(miny, maxy + 1):
        count = count + evaluate_line(y, intervals)
    print('capacity for part one is {}'.format(count))

    cx, cy = 0, 0
    intervals = []
    for line in lines:
        _, _, color = line.split()
        dist = int(color[2:7], 16)
        dir = color[7]
        if dir == '0': cx = cx + dist
        if dir == '2': cx = cx - dist
        if dir == '1':
            ncy = cy + dist
            intervals.append((cx, cy, ncy))
            cy = ncy
        if dir == '3':
            ncy = cy - dist
            intervals.append((cx, ncy, cy))
            cy = ncy

    intervals = sorted(intervals)
    miny = min([i[1] for i in intervals])
    maxy = max([i[2] for i in intervals])
    print('miny = {}, maxy = {}'.format(miny, maxy))

    # This is rather slow, but it is fast enough.
    # A faster solution would identify which y values have vertices
    # and only evaluate them.
    count = 0
    for y in range(miny, maxy + 1):
        if y % 100000 == 0: print('tested to y {}...'.format(y))
        count = count + evaluate_line(y, intervals)
    print('capacity for part two is {}'.format(count))

