import sys

numbers = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    sum = 0
    for line in lines:
        line = line.strip()
        first = -1
        last = -1
        for c in line:
            if c.isdigit():
                if first < 0:
                    first = int(c)
                last = int(c)
        sum = sum + first * 10 + last

    print('the sum for part one is {}'.format(sum))

    sum = 0
    for line in lines:
        line = line.strip()
        first = -1
        last = -1
        c = 0
        while c < len(line):
            num = -1
            for n in numbers:
                if line[c:].startswith(n):
                    num = numbers[n]
                    break
            if num < 1:
                if line[c].isdigit():
                    num = int(line[c])
            c = c + 1
            if num >= 0:
                if first < 0:
                    first = num
                last = num
        #print('calibration value for {} is {}'.format(line, first * 10 + last))
        sum = sum + first * 10 + last

    print('the sum for part two is {}'.format(sum))
