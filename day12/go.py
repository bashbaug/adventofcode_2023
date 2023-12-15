import sys

def do_count(record, counts, c):
    if c >= len(record):
        check = [len(x) for x in record.replace('.', ' ').split()]
        if check == counts:
            return 1
        else:
            return 0

    if record[c] == '?':
        check0 = record[:c] + '.' + record[c + 1:]
        return do_count(check0, counts, c+1) + do_count(record, counts, c + 1)

    return do_count(record, counts, c + 1)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        record, counts = line.strip().split()
        counts = [int(x) for x in counts.split(',')]
        print('checking record {}...'.format(record))
        count = do_count(record, counts, 0)
        print('  --> {} arrangements'.format(count))
        total = total + count

    print('total count for part one is: {}'.format(count))


    total = 0
    for line in lines:
        record, counts = line.strip().split()
        record = record + '?' + record + '?' + record + '?' + record + '?' + record
        counts = [int(x) for x in counts.split(',')]
        counts = counts * 5
        print('checking record {}...'.format(record))
        count = do_count(record, counts, 0)
        print('  --> {} arrangements'.format(count))
        total = total + count

    print('total count for part one is: {}'.format(count))
