import sys

def issymbol(v):
    if v.isdigit(): return False
    if v == '.': return False
    if v.isspace(): return False
    return True

def check_coord(lines, r, c):
    if r < 0 or r >= len(lines): return False, '.'
    if c < 0 or c >= len(lines[0]): return False, '.'
    return issymbol(lines[r][c]), lines[r][c]

def has_adjacent_symbol(lines, r, c):
    for rd in [-1, 0, 1]:
        for cd in [-1, 0, 1]:
            check, symbol = check_coord(lines, r + rd, c + cd)
            if check:
                return check, symbol, r + rd, c + cd
    return False, ',', 0, 0

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    part_numbers = []
    gears = {}
    for row, line in enumerate(lines):
        col = 0
        while col < len(line):
            part_number = 0
            is_part_number = False
            is_gear = False
            grow = 0
            gcol = 0
            while col < len(line) and line[col].isdigit():
                part_number = part_number * 10 + int(line[col])
                check, symbol, srow, scol = has_adjacent_symbol(lines, row, col)
                is_part_number = is_part_number or check
                if symbol == '*':
                    #print('found gear at {}, {}'.format(srow, scol))
                    is_gear = True
                    grow = srow
                    gcol = scol
                col = col + 1
            if part_number != 0:
                if is_part_number:
                    #print('{} is a part number'.format(part_number))
                    part_numbers.append(part_number)
                #else:
                #    print('{} is NOT a part number!'.format(part_number))
            if is_gear:
                gears.setdefault((grow, gcol), [])
                gears[(grow, gcol)].append(part_number)
                #print('found part number {} next to gear at {}, {}'.format(part_number, grow, gcol))
            col = col + 1
        #print()

    print('the sum of part numbers for part one is: {}'.format(sum(part_numbers)))

    sum = 0
    for gparts in gears:
        if len(gears[gparts]) == 2:
            #print('there are two parts next to gear at {}: {}'.format(gparts, gears[gparts]))
            gear_ratio = gears[gparts][0] * gears[gparts][1]
            #print('gear ratio is {}'.format(gear_ratio))
            sum = sum + gear_ratio

    print('the sum of gear ratios for part two is {}'.format(sum))
