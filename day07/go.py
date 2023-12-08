import sys

card_to_rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
card_to_rank2 = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':1, 'Q':12, 'K':13, 'A':14}

def evaluate_hand(hand):
    shand = ''.join(sorted(hand))

    if shand[0] == shand[1]:
        match = 0
    elif shand[1] == shand[2]:
        match = 1
    elif shand[2] == shand[3]:
        match = 2
    elif shand[3] == shand[4]:
        match = 3
    else:
        return 1    # no matches, high card
    
    test = shand.replace(shand[match], '')
    if len(test) == 0:
        return 100  # five of a kind
    if len(test) == 1:
        return 50   # four of a kind
    if len(test) == 2:
        test = test.replace(test[0], '')
        if len(test) == 0:
            return 40   # full house
        else:
            return 30   # three of a kind
    if len(test) == 3:
        test0 = test.replace(test[0], '')
        test1 = test.replace(test[1], '')
        if len(test0) == 0:
            return 40   # full house
        elif len(test0) == 1 or len(test1) == 1:
            return 20   # two pair
        else:
            return 10   # one pair

    return 10   # one pair

def evaluate_hand2(hand):
    shand = ''.join(sorted(hand))

    test = shand.replace('J', '')
    if len(test) == 5:  # no jokers
        return evaluate_hand(hand)
    if len(test) == 0 or len(test) == 1:  # four or five jokers
        return 100
    
    temp_hand = [chr(ord('a') + i) if c == 'J' else c for i, c in enumerate(shand)]
    shand = ''.join(temp_hand)
    
    score = 0
    temp_score = evaluate_hand(shand)
    if len(test) == 4:    # one joker
        score = 100 if temp_score == 50 else score  # four of a kind to five of a kind
        score =  50 if temp_score == 30 else score  # three of a kind to four of a kind
        score =  40 if temp_score == 20 else score  # two pair to full house
        score =  30 if temp_score == 10 else score  # one pair to three of a kind
        score =  10 if temp_score ==  1 else score  # high card to one pair
    elif len(test) == 3:  # two jokers
        score = 100 if temp_score == 30 else score  # three of a kind to five of a kind
        score =  50 if temp_score == 10 else score  # one pair to four of a kind
        score =  30 if temp_score ==  1 else score  # high card to three of a kind
    elif len(test) == 2:  # three jokers
        score = 100 if temp_score == 10 else score  # one pair to five of a kind
        score =  50 if temp_score ==  1 else score  # high card to four of a kind

    return score


def hand_sort_key(hand):
    return [hand[0]] + [card_to_rank[c] for c in hand[1]]

def hand_sort_key2(hand):
    return [hand[0]] + [card_to_rank2[c] for c in hand[1]]

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append([evaluate_hand(hand), hand, int(bid)])

    hands = sorted(hands, key=hand_sort_key)

    winnings = sum([(i + 1) * hand[2] for i, hand in enumerate(hands)])
    print('total winnings are: {}'.format(winnings))

    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append([evaluate_hand2(hand), hand, int(bid)])

    hands = sorted(hands, key=hand_sort_key2)

    winnings = sum([(i + 1) * hand[2] for i, hand in enumerate(hands)])
    print('total winnings with jokers are: {}'.format(winnings))
