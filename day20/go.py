import sys
import collections

FLIP_FLOP = '%'
CONJUNCTION = '&'

FF_OFF = False
FF_ON = True

PULSE_LO = 0
PULSE_HI = 1

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    config = {}
    for line in lines:
        namestr, dststr = line.split('->')
        namestr = namestr.strip()
        dsts = [s.strip() for s in dststr.split(',')]
        if namestr == 'broadcaster':
            config['broadcaster'] = {'type':'broadcaster', 'dsts':dsts}
        else:
            name = namestr[1:]
            type = namestr[0]
            config[name] = {'type':type, 'dsts':dsts, 'inputs':[]}

    debugs = []
    for key in config:
        for dst in config[key]['dsts']:
            if dst not in config:
                debugs.append(dst)

    for debug in debugs:
        config[debug] = {'type':'debug', 'dsts':[], 'inputs':[]}

    last_pulse = {}
    state = {}
    for key in config:
        for dst in config[key]['dsts']:
            config[dst]['inputs'].append(key)
        last_pulse[key] = PULSE_LO
        state[key] = FF_OFF

    count_lo = 0
    count_hi = 0
    presses = 0
    while True:
        presses = presses + 1
        if presses % 100000 == 0:
            print('tested {} presses...'.format(presses))

        #print('pressing button, i = {}, low count is {}, high count is {}...'.format(i, count_lo, count_hi))
        work_list = collections.deque()

        lo_to_rx = 0

        #print('\t{} is sending {} to {}'.format('button', PULSE_LO, 'broadcaster'))
        work_list.appendleft({'dst':'broadcaster', 'pulse':PULSE_LO})
        last_pulse['button'] = PULSE_LO
        while len(work_list) != 0:
            command = work_list.pop()

            dst = command['dst']
            pulse = command['pulse']

            if pulse == PULSE_LO: count_lo = count_lo + 1
            if pulse == PULSE_HI: count_hi = count_hi + 1

            type = config[dst]['type']
            if type == 'broadcaster':
                newpulse = pulse
                for d in config[dst]['dsts']:
                    #print('\t{} is sending {} to {}'.format(dst, newpulse, d))
                    work_list.appendleft({'dst':d, 'pulse':newpulse})
                last_pulse['broadcaster'] = newpulse
            elif type == 'debug':
                pass
            elif type == FLIP_FLOP:
                if pulse == PULSE_LO:
                    newpulse = PULSE_HI if state[dst] == FF_OFF else PULSE_LO
                    for d in config[dst]['dsts']:
                        #print('\t{} is sending {} to {}'.format(dst, newpulse, d))
                        work_list.appendleft({'dst':d, 'pulse':newpulse})
                    state[dst] = not state[dst]
                    last_pulse[dst] = newpulse
            elif type == CONJUNCTION:
                newpulse = PULSE_LO
                for s in config[dst]['inputs']:
                    if last_pulse[s] == PULSE_LO:
                        newpulse = PULSE_HI
                        break
                for d in config[dst]['dsts']:
                    #print('\t{} is sending {} to {}'.format(dst, newpulse, d))
                    work_list.appendleft({'dst':d, 'pulse':newpulse})
                last_pulse[dst] = newpulse
                
                if 'rx' in config and dst == 'sb' and newpulse == PULSE_HI:
                    print('{} outputted HIGH on press {}'.format(dst, presses))
                if 'rx' in config and dst == 'nd' and newpulse == PULSE_HI:
                    print('{} outputted HIGH on press {}'.format(dst, presses))
                if 'rx' in config and dst == 'ds' and newpulse == PULSE_HI:
                    print('{} outputted HIGH on press {}'.format(dst, presses))
                if 'rx' in config and dst == 'hf' and newpulse == PULSE_HI:
                    print('{} outputted HIGH on press {}'.format(dst, presses))
            else:
                print('UNEXPECTED TYPE!')

        if presses == 1000:
            print('after 1000 button presses: lo = {}, hi = {}, product = {}'.format(count_lo, count_lo, count_lo * count_hi))
            if 'rx' not in config:
                print('skipping part two, there is no module named rx')
                break

        if presses == 10000:
            break

# for part two: found how often each input cycled, then found lcm of those inputs.
# sb = 3797, nd = 3917, ds = 3733, hf = 3877, math.lcm() of these values is 215252378794009