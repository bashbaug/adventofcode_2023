import sys

def evaluate_forward(seq):
    new_seq = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    return seq[-1] + (evaluate_forward(new_seq) if any(x != 0 for x in new_seq) else 0)

def evaluate_backward(seq):
    new_seq = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    return seq[0] - (evaluate_backward(new_seq) if any(x != 0 for x in new_seq) else 0)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        seq = [int(x) for x in line.split()]
        #print('sequence is: {}'.format(seq))
        vf = evaluate_forward(seq)
        #print('extrapolated forward value is: {}'.format(vf))
        total = total + vf

    print('total value for part one is: {}'.format(total))

    total = 0
    for line in lines:
        seq = [int(x) for x in line.split()]
        #print('sequence is: {}'.format(seq))
        vb = evaluate_backward(seq)
        #print('extrapolated backward value is: {}'.format(vb))
        total = total + vb

    print('total value for part two is: {}'.format(total))
