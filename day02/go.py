import sys

num_cubes = {'red':12, 'green':13, 'blue':14}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    sum_valid = 0
    sum_power = 0
    for game, line in enumerate(lines):
        reveals = line.split(':')[1].split(';')
        max_cubes = {'red':0, 'green':0, 'blue':0}
        for reveal in reveals:
            cubes = reveal.split(',')
            for cube in cubes:
                [count, color] = cube.strip().split(' ')
                max_cubes[color] = max(max_cubes[color], int(count))
        valid = True
        power = 1
        for color in max_cubes:
            valid = valid and max_cubes[color] <= num_cubes[color]
            power = power * max_cubes[color]
        if valid:
            sum_valid = sum_valid + int(game) + 1
        sum_power = sum_power + power
    print('the sum for part 1 is {}'.format(sum_valid))
    print('the sum for part 2 is {}'.format(sum_power))
