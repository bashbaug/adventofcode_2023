import sys
import copy

def brick_sort_key(brick):
    return brick[0][2]

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    bricks = []
    maxx = 0
    maxy = 0
    for i, line in enumerate(lines):
        coord0, coord1 = line.strip().split('~')
        coord0 = [int(x) for x in coord0.split(',')]
        coord1 = [int(x) for x in coord1.split(',')]
        #print('brick {}: {} to {}'.format(i, coord0, coord1))
        # note: all bricks are ordered!
        bricks.append((coord0, coord1))
        maxx = max(maxx, coord1[0])
        maxy = max(maxy, coord1[1])

    #print('maxx = {}, maxy = {}'.format(maxx, maxy))
    bricks = sorted(bricks, key=brick_sort_key)
    print('there are {} bricks'.format(len(bricks)))

    stacks = {}
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            stacks[(x, y)] = (0, -1)    # height, id

    supports = {}
    supports[-1] = set()
    supported_by = {}
    supported_by[-1] = set()
    for b, brick in enumerate(bricks):
        # find the height of this brick
        height = 0
        for y in range(brick[0][1], brick[1][1] + 1):
            for x in range(brick[0][0], brick[1][0] + 1):
                height = max(height, stacks[(x, y)][0] + 1)

        supports[b] = set()
        supported_by[b] = set()
        
        #print('brick {} sits at height {}'.format(b, height))
        newheight = height + brick[1][2] - brick[0][2]
        for y in range(brick[0][1], brick[1][1] + 1):
            for x in range(brick[0][0], brick[1][0] + 1):
                if stacks[(x, y)][0] == height - 1:
                    base = stacks[(x, y)][1]
                    supports[base].add(b)
                    supported_by[b].add(base)
                stacks[(x, y)] = (newheight, b)

    supports.pop(-1)
    supported_by.pop(-1)
    #print('supports: {}'.format(supports))
    #print('supported_by: {}'.format(supported_by))

    count = 0
    nonredundant = set()
    for s, check in enumerate(supports):
        working = copy.deepcopy(supports[check])
        for o, other in enumerate(supports):
            if s != o:
                working = working.difference(supports[other])
        if len(working) == 0:
            #print('brick {} is redundant'.format(s))
            count = count + 1
        else:
            nonredundant.add(check)

    print('there are {} redundant bricks'.format(count))
    #print('there are {} nonredundant bricks'.format(len(nonredundant)))
    #print('nonredundant bricks: {}'.format(nonredundant))

    count = 0
    for b in nonredundant:
        #print('checking reaction for brick {}'.format(b))
        working_count = 0
        working = copy.deepcopy(supported_by)
        working[b] = set()
        for check in range(b, len(bricks)):
            if len(working[check]) == 0:
                working_count = working_count + 1
                #print('brick {} falls'.format(check))
                for other in supports[check]:
                    working[other].remove(check)
        #print('    {} bricks fell'.format(working_count))
        count = count + working_count - 1

    print('a total of {} bricks fell'.format(count))
