import sys

def find_longest(record):
    longest = []
    for c in range(len(record)):
        run = 0
        for i in range(c, len(record)):
            if record[i] == '.':
                break
            run = run + 1
        longest.append(run)
    return longest

def find_min_remaining(record):
    remaining = []
    for c in range(len(record)):
        started = False
        count = 0
        for i in range(c, len(record)):
            if record[i] == '#':
                started = True
            if record[i] == '.' and started:
                started = False
                count = count + 1
        if started:
            count = count + 1
        remaining.append(count)
    return remaining

# r is the working character
# w is the working count
def do_count(cache, record, counts, longest, remaining, r, c):
    if (r, c) in cache:
        return cache[(r, c)]

    if c > len(counts):
        return 0
    
    while r < len(record) and record[r] == '.':
        r = r + 1

    if r >= len(record):
        if c == len(counts):
            return 1
        else:
            return 0
        
    if c + remaining[r] > len(counts):
        return 0

    alternate = 0
    if record[r] == '?':
        alternate = do_count(cache, record, counts, longest, remaining, r + 1, c)

    if c >= len(counts):
        cache[(r, c)] = alternate
        return alternate

    target = counts[c]
    if longest[r] < target:
        cache[(r, c)] = alternate
        return alternate

    if r + target < len(record) and record[r + target] == '#':
        cache[(r, c)] = alternate
        return alternate

    alternate = alternate + do_count(cache, record, counts, longest, remaining, r + target + 1, c + 1)
    cache[(r, c)] = alternate
    return alternate

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        record, counts = line.strip().split()
        counts = [int(x) for x in counts.split(',')]
        longest = find_longest(record)
        remaining = find_min_remaining(record)
        count = do_count({}, record, counts, longest, remaining, 0, 0)
        total = total + count
    
    print('total count for part one is: {}'.format(total))


    total = 0
    for line in lines:
        record, counts = line.strip().split()
        record = record + '?' + record + '?' + record + '?' + record + '?' + record
        counts = [int(x) for x in counts.split(',')]
        counts = counts * 5
        longest = find_longest(record)
        remaining = find_min_remaining(record)
        count = do_count({}, record, counts, longest, remaining, 0, 0)
        total = total + count

    print('total count for part two is: {}'.format(total))
