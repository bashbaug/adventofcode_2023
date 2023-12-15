import sys

def check_v_reflection(pattern, col, num):
    mismatches = 0
    for line in pattern:
        for i in range(col + 1):
            l = col - i
            r = col + i + 1
            if l < 0 or r >= len(line):
                continue
            if line[l] != line[r]:
                mismatches = mismatches + 1
    return mismatches == num

def find_v_reflection(pattern, num):
    for col in range(len(pattern[0]) - 1):
        if check_v_reflection(pattern, col, num):
            return col + 1
    return 0

def check_h_reflection(pattern, row, num):
    mismatches = 0
    for i in range(row + 1):
        t = row - i
        b = row + i + 1
        if t < 0 or b >= len(pattern):
            continue
        for c in range(len(pattern[0])):
            if pattern[t][c] != pattern[b][c]:
                mismatches = mismatches + 1
    return mismatches == num

def find_h_reflection(pattern, num):
    for row in range(len(pattern) - 1):
        if check_h_reflection(pattern, row, num):
            return row + 1
    return 0

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    lines.append('')

    total = 0
    pattern = []
    for line in lines:
        if line.strip() == '':
            col = find_v_reflection(pattern, 0)
            row = find_h_reflection(pattern, 0)
            #print('***** col = {}, row = {}'.format(col, row))
            total = total + col + 100 * row
            pattern = []
        else:
            pattern.append(line.strip())

    print('total count for part one is: {}'.format(total))

    total = 0
    pattern = []
    for line in lines:
        if line.strip() == '':
            col = find_v_reflection(pattern, 1)
            row = find_h_reflection(pattern, 1)
            #print('***** col = {}, row = {}'.format(col, row))
            total = total + col + 100 * row
            pattern = []
        else:
            pattern.append(line.strip())

    print('total count for part two is: {}'.format(total))
