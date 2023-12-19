import sys
import re
import copy

def test_item(rules, item):
    state = 'in'
    while True:
        if state == 'A':
            return True
        if state == 'R':
            return False
        rule = rules[state]
        state = rule['default']
        for cond in rule['conditions']:
            if cond['op'] == '<':
                if item[cond['attrib']] < cond['value']:
                    state = cond['goto']
                    break
            elif cond['op'] == '>':
                if item[cond['attrib']] > cond['value']:
                    state = cond['goto']
                    break
    return False

def trace_ranges(rules, state, ranges):
    if state == 'A':
        return ((ranges['x']['max'] - ranges['x']['min'] + 1) *
                (ranges['m']['max'] - ranges['m']['min'] + 1) *
                (ranges['a']['max'] - ranges['a']['min'] + 1) *
                (ranges['s']['max'] - ranges['s']['min'] + 1))
    if state == 'R':
        return 0
    
    rule = rules[state]
    count = 0
    for cond in rule['conditions']:
        if cond['op'] == '<':
            attrib = cond['attrib']
            value = cond['value']
            if ranges[attrib]['min'] >= value:
                # trivial reject
                pass
            elif ranges[attrib]['max'] < value:
                # trivial accept
                return count + trace_ranges(rules, cond['goto'], ranges)
            else:
                # split
                newranges = copy.deepcopy(ranges)
                newranges[attrib]['max'] = value - 1
                count = count + trace_ranges(rules, cond['goto'], newranges)

                ranges[attrib]['min'] = value
        elif cond['op'] == '>':
            attrib = cond['attrib']
            value = cond['value']
            if ranges[attrib]['max'] <= value:
                # trivial reject
                pass
            elif ranges[attrib]['min'] > value:
                # trivial accept
                return count + trace_ranges(rules, cond['goto'], ranges)
            else:
                # split
                newranges = copy.deepcopy(ranges)
                newranges[attrib]['min'] = value + 1
                count = count + trace_ranges(rules, cond['goto'], newranges)

                ranges[attrib]['max'] = value
    return count + trace_ranges(rules, rule['default'], ranges)

if __name__ == "__main__":
    rules = {}
    total_accepted = 0
    with open(sys.argv[1]) as f:
        while True:
            line = f.readline().strip()
            if line == '': break

            name, transition_strings, _ = re.split('{|}', line)
            transition_strings = transition_strings.split(',')

            rule = {}
            rule['conditions'] = []
            for transition_string in transition_strings:
                if ':' in transition_string:
                    condition = {}
                    condition_string, state = transition_string.split(':')
                    condition['attrib'] = condition_string[0]
                    condition['op'] = condition_string[1]
                    condition['value'] = int(condition_string[2:])
                    condition['goto'] = state
                    rule['conditions'].append(condition)
                else:
                    rule['default'] = transition_string
            rules[name] = rule

        while True:
            line = f.readline().strip()
            if line == '': break

            item = {}
            total = 0
            for astr in line[1:-1].split(','):
                a, v = astr.split('=')
                v = int(v)
                item[a] = v
                total = total + v

            #print('item: {}'.format(item))
            if test_item(rules, item):
                total_accepted = total_accepted + total

    print('total accepted for part one is: {}'.format(total_accepted))

    ranges = {'x':{'min':1,'max':4000}, 'm':{'min':1,'max':4000}, 'a':{'min':1,'max':4000}, 's':{'min':1,'max':4000}}
    count = trace_ranges(rules, 'in', ranges)
    print('total count for part two is: {}'.format(count))
