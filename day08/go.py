import sys
import math

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    instructions = lines[0].strip()

    nodes = {}
    for line in lines[2:]:
        node = line[0:3]
        l = line[7:10]
        r = line[12:15]
        nodes[node] = (l, r)

    if 'AAA' in nodes:
        location = 'AAA'
        step = 0
        while location != 'ZZZ':
            direction = instructions[step % len(instructions)]
            if direction == 'L':
                location = nodes[location][0]
            elif direction == 'R':
                location = nodes[location][1]
            step = step + 1
        print('found destination ZZZ in {} steps'.format(step))

    ghostnodes = []
    for location in nodes:
        if location[2] == 'A':
            ghostnodes.append(location)

    print('ghost nodes are {}'.format(ghostnodes))

    pathlengths = [0] * len(ghostnodes)
    step = 0
    while min(pathlengths) == 0:
        newghostnodes = []
        direction = instructions[step % len(instructions)]
        step = step + 1
        for i, location in enumerate(ghostnodes):
            if direction == 'L':
                location = nodes[location][0]
            elif direction == 'R':
                location = nodes[location][1]
            if location[2] == 'Z' and pathlengths[i] == 0:
                pathlengths[i] = step
            newghostnodes.append(location)
        ghostnodes = newghostnodes

    print('path lengths are {}'.format(pathlengths))
    step = math.lcm(*pathlengths)

    print('ghosts reached destination after {} steps'.format(step))

