
from aocd import data, post
from functools import cmp_to_key
from collections import Counter

input = data.split('\n')

hands = [l.split() for l in input]

def kind(hand):
    s = set(hand)
    m = max(Counter(hand).values())

    if len(s) == 1:
        return 7

    if len(s) == 2:
        if m == 4:
            return 6
        return 5

    if len(s) == 3:
        if m == 3:
            return 4
        return 3

    if len(s) == 4:
        return 2
    if len(s) == 5:
        return 1

z = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
val = {z[i]:-i for i in range(len(z))}

def compare(kind, hand1, hand2):
    hand1 = hand1[0]
    hand2 = hand2[0]
    k1 = kind(hand1)
    k2 = kind(hand2)
    if k1 > k2:
        return 1
    elif k1 < k2:
        return -1
    
    for i in range(len(hand1)):
        if val[hand1[i]] < val[hand2[i]]:
            return -1
        if val[hand1[i]] > val[hand2[i]]:
            return 1

hands = sorted(hands, key=cmp_to_key(lambda x, y: compare(kind, x, y)))

r1 = sum(((ci+1) * int(hands[ci][1]) for ci in range(len(hands))))

post.submit(r1, part="a", day=7)

r2 = 0

z = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
val = {z[i]:-i for i in range(len(z))}

def kind2(hand):
    s = set(hand).difference(['J'])
    if len(s) == 0:
        return 7

    return max((kind(hand.replace('J', e)) for e in s))

hands = sorted(hands, key=cmp_to_key(lambda x, y: compare(kind2, x, y)))

r2 = sum(((ci+1) * int(hands[ci][1]) for ci in range(len(hands))))

post.submit(r2, part="b", day=7)
