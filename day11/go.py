import sys

def col_has_galaxy(lines, c):
    for line in lines:
        if line[c] == '#':
            return True
    return False

def row_has_galaxy(lines, r):
    for c in lines[r]:
        if c == '#':
            return True
    return False

def distance_bonus(expansions, start, end, value):
    s = start if start < end else end
    e = end if start < end else start
    bonus = 0
    for v in range(s, e):
        if v in expansions:
            bonus = bonus + value
    return bonus

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    expansion_cols = [c for c in range(len(lines[0])) if col_has_galaxy(lines, c) == False]
    #print('expansion cols are: {}'.format(expansion_cols))

    expansion_rows = [r for r in range(len(lines)) if row_has_galaxy(lines, r) == False]
    #print('expansion rows are: {}'.format(expansion_rows))

    galaxies = [(r, c) for r, line in enumerate(lines) for c, val in enumerate(line) if val == '#']
    #print('found galaxies at: {}'.format(galaxies))

    distance = 0
    for g, start in enumerate(galaxies):
        for end in galaxies[:g]:
            d = abs(start[0] - end[0])
            d = d + abs(start[1] - end[1])
            d = d + distance_bonus(expansion_rows, start[0], end[0], 1)
            d = d + distance_bonus(expansion_cols, start[1], end[1], 1)
            distance = distance + d
    
    print('total distance for part one is: {}'.format(distance))

    distance = 0
    for g, start in enumerate(galaxies):
        for end in galaxies[:g]:
            d = abs(start[0] - end[0])
            d = d + abs(start[1] - end[1])
            d = d + distance_bonus(expansion_rows, start[0], end[0], 1000000-1)
            d = d + distance_bonus(expansion_cols, start[1], end[1], 1000000-1)
            distance = distance + d
    
    print('total distance for part two is: {}'.format(distance))

