import sys

def intersect(winners, have):
    return set(winners).intersection(have)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    points = 0
    counts = {}
    for n, line in enumerate(lines):
        n = n + 1
        counts.setdefault(n, 0)
        counts[n] = counts[n] + 1
        card, numbers = line.strip().split(':')
        winners, have = numbers.strip().split('|')
        winners = winners.strip().split()
        have = have.strip().split()
        #print('for {}: winners = {}, have = {}'.format(card, winners, have))
        common = intersect(winners, have)
        #print('    common = {}'.format(common))
        matches = len(common)
        score = 0 if matches == 0 else 2 ** (matches - 1)
        #print('    score = {}'.format(score))
        points = points + score
        for i in range(matches):
            counts.setdefault(n + i + 1, 0)
            counts[n + i + 1] = counts[n] + counts[n + i + 1]

    cards = 0
    for count in counts:
        #print('count for card {} is {}'.format(count, counts[count]))
        cards = cards + counts[count]

    print('the sum for part one is: {}'.format(points))
    print('the sum for part two is: {}'.format(cards))