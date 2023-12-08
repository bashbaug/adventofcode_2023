import sys

def count_wins(time, record):
    wins = 0
    for t in range(1, time):
        distance = t * (time - t)
        if distance > record:
            wins = wins + 1
    return wins

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    times = [int(x) for x in lines[0].split(':')[1].split()]
    records = [int(x) for x in lines[1].split(':')[1].split()]

    product = 1
    for race in range(len(times)):
        product = product * count_wins(times[race], records[race])

    print('product of wins for part one is: {}'.format(product))

    time = int(lines[0].split(':')[1].replace(' ',''))
    record = int(lines[1].split(':')[1].replace(' ', ''))

    print('number of wins for part two is: {}'.format(count_wins(time, record)))
