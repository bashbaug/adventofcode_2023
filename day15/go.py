import sys
from collections import OrderedDict

def compute_hash(step):
    current = 0
    for c in step:
        current = current + ord(c)
        current = current * 17
        current = current % 256
    return current

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    total = 0
    sequences = lines[0].strip().split(',')
    for step in sequences:
        result = compute_hash(step)
        total = total + result

    print('total for part one is: {}'.format(total))

    boxes = []
    for i in range(256):
        boxes.append(OrderedDict())
    for step in sequences:
        if '=' in step:
            label, lens = step.split('=')
            box = compute_hash(label)
            boxes[box][label] = lens
        else:
            label, _ = step.split('-')
            box = compute_hash(label)
            if label in boxes[box]:
                boxes[box].pop(label)

    total = 0
    for num, box in enumerate(boxes):
        for slot, lens in enumerate(box.values()):
            fp = (num + 1) * (slot + 1) * int(lens)
            total = total + fp

    print('total for part two is: {}'.format(total))
