import sys
import copy
import matplotlib.path

def setpath(lines, c):
    v = lines[c[1]][c[0]]
    line = lines[c[1]]
    line = line[:c[0]] + '#' + line[c[0] + 1:]
    lines[c[1]] = line
    return v

def check_left(c, lines, distance, points):
    distance = distance + 1
    c = (c[0] - 1, c[1])
    v = lines[c[1]][c[0]]
    setpath(lines, c)
    if v == 'S':
        points.append(c)
        return distance, points
    if v == '-':
        return check_left(c, lines, distance, points)
    if v == 'L':
        points.append(c)
        return check_up(c, lines, distance, points)
    if v == 'F':
        points.append(c)
        return check_down(c, lines, distance, points)
    return -1, points

def check_right(c, lines, distance, points):
    distance = distance + 1
    c = (c[0] + 1, c[1])
    v = setpath(lines, c)
    if v == 'S':
        points.append(c)
        return distance, points
    if v == '-':
        return check_right(c, lines, distance, points)
    if v == 'J':
        points.append(c)
        return check_up(c, lines, distance, points)
    if v == '7':
        points.append(c)
        return check_down(c, lines, distance, points)
    return -1, points

def check_up(c, lines, distance, points):
    distance = distance + 1
    c = (c[0], c[1] - 1)
    v = setpath(lines, c)
    if v == 'S':
        points.append(c)
        return distance, points
    if v == '7':
        points.append(c)
        return check_left(c, lines, distance, points)
    if v == 'F':
        points.append(c)
        return check_right(c, lines, distance, points)
    if v == '|':
        return check_up(c, lines, distance, points)
    return -1, points

def check_down(c, lines, distance, points):
    distance = distance + 1
    c = (c[0], c[1] + 1)
    v = setpath(lines, c)
    if v == 'S':
        points.append(c)
        return distance, points
    if v == 'J':
        points.append(c)
        return check_left(c, lines, distance, points)
    if v == 'L':
        points.append(c)
        return check_right(c, lines, distance, points)
    if v == '|':
        return check_down(c, lines, distance, points)
    return -1, points

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    blank = '.' * len(lines[0].strip())
    lines.insert(0, blank)
    lines.append(blank)
    for i, line in enumerate(lines):
        lines[i] = '.' + line.strip() + '.'

    c = [(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == 'S'][0]

    working = copy.deepcopy(lines)
    distance, points = check_left(c, working, 0, [])
    if distance <= 0:
        working = copy.deepcopy(lines)
        distance, points = check_right(c, working, 0, [])
    if distance <= 0:
        working = copy.deepcopy(lines)
        distance, points = check_up(c, working, 0, [])
    if distance <= 0:
        working = copy.deepcopy(lines)
        distance, points = check_down(c, working, 0, [])

    distance = distance // 2
    print('longest distance for part one is: {}'.format(distance))

    path = matplotlib.path.Path(points)
    enclosed = sum([1 for y, line in enumerate(working) for x, c in enumerate(line) if c != '#' and path.contains_point((x, y))])
    print('number of enclosed tiles is: {}'.format(enclosed))