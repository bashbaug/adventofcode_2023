import sys

def evaluate_interval(all_intervals, depth, start, end):
    if depth >= len(all_intervals):
        return start
    for [d, s, e] in all_intervals[depth]:
        # there are six cases:
        # 1) completely too low, continue.
        if end < s: continue
        # 2) completely too high, continue.
        if start >= e: continue
        # 3) enclosed, adjust and go deeper.
        if start >= s and end <= e:
            newstart = start + d - s
            newend = end + d - s
            return evaluate_interval(all_intervals, depth + 1, newstart, newend)
        # 4) min side, split and reevaluate.
        if start < s and end <= e:
            left = evaluate_interval(all_intervals, depth, start, s - 1)
            right = evaluate_interval(all_intervals, depth, s, end)
            return min(left, right)
        # 5) max side, split and reevaluate.
        if start >= s and end > e:
            left = evaluate_interval(all_intervals, depth, start, e - 1)
            right = evaluate_interval(all_intervals, depth, e, end)
            return min(left, right)
        # 6) span, split and reevaluate
        if start < s and end > e:
            left = evaluate_interval(all_intervals, depth, start, s - 1)
            mid = evaluate_interval(all_intervals, depth, s, e - 1)
            right = evaluate_interval(all_intervals, depth, e, end)
            return min(left, mid, right)
        # this shouldn't happen
        return 0
    # did not intersect any intervals, onwards
    return evaluate_interval(all_intervals, depth + 1, start, end)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    lines.append('\n')

    seeds = [int(x) for x in lines[0].split(':')[1].split()]
    all_intervals = []
    intervals = []
    for line in lines[2:]:
        if line[0].isalpha():
            continue
        if line[0].isdigit():
            [d, s, l] = [int(x) for x in line.split()]
            intervals.append([d, s, s + l])
            continue
        all_intervals.append(intervals[:])
        intervals.clear()

    minval = sys.maxsize
    for v in seeds:
        result = evaluate_interval(all_intervals, 0, v, v)
        minval = min(minval, result)

    print('minimum location for part one is {}'.format(minval))

    minval = sys.maxsize
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        end = start + seeds[i+1]
        result = evaluate_interval(all_intervals, 0, start, end)
        minval = min(minval, result)

    print('minimum location for part two is {}'.format(minval))