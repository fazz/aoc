
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter
from itertools import chain, combinations
from math import factorial
import operator
import re
import sys

from aoc import factor

input = data.split('\n')

def checknumbers(filledpattern, expected, extra=tuple()):
    s = 0
    count = 0
    i = 0
    mi = len(expected) - 1

    for ci in range(len(filledpattern)):
        c = filledpattern[ci]
        if (c == '#' or ci in extra):
            if s == 0:
                s = 1
                count = 1
            else:
                count += 1
        elif c in ('.', '?') and s == 1:
            if not (i <= mi and expected[i] == count):
                return False
            count = 0
            s = 0
            i += 1

    if s == 1:
        if not (i <= mi and expected[i] == count):
            return False
        i += 1

    if i != mi+1:
        return False

    return True

precalc = {}
def calc(pattern, numbers):
    global precalc

    if (pattern, numbers) in precalc:
        return precalc[(pattern, numbers)]

    number = numbers[0]

    qm = len([c for c in pattern if c == '?'])

    reqd = sum(numbers) - len([c for c in pattern if c == '#'])

    if reqd < 0 or qm < reqd:
        return 0
    elif reqd == 0:
        if checknumbers(pattern, numbers):
            return 1
        else:
            return 0
    elif pattern[0] == '.':
        count = calc(pattern[1:], numbers)
        precalc[(pattern, numbers)] = count
    else:
        if '#' in pattern:
            pi = pattern.index('#')
        else:
            pi = len(pattern)

        if len(numbers) == 1:
            start = 0
            if '#' in pattern:
                start = pi - number + 1
            end = min(pi+1, len(pattern)-number+1)
        else:
            end = min(pi+1, len(pattern)-number-len(numbers[2:])-sum(numbers[1:]))

        count = 0

        if len(numbers) == 1:
            for i in range(start, end):
                if not '.' in pattern[i:i+number] and (i+number == len(pattern) or pattern[i+number] != '#'):
                    if checknumbers(pattern, numbers, extra=range(i, i+number)):
                        count += 1
        else:
            for i in range(0, end):
                if not '.' in pattern[i:i+number] and (i+number == len(pattern) or pattern[i+number] != '#'):
                    count += calc(pattern[i+number+1:], numbers[1:])

        precalc[(pattern, numbers)] = count

    return count

r1 = 0
r2 = 0

for l in input:
    (p, n) = l.split()
    n = tuple(map(int, n.split(',')))

    p2 = p
    n2 = n

    for _ in range(4):
        p2 = p2 + '?' + p
        n2 = n2 + n

    precalc = {}

    r1 += calc(p,n)
    r2 += calc(p2,n2)

print("r1:", r1)
print("r2:", r2)

post.submit(r1, part="a", day=12)
post.submit(r2, part="b", day=12)
