
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter, deque
from itertools import chain
from math import inf
import operator
import re
import sys

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

from aoc import factor

input = data.split('\n')

oneside = 65
steps = 26501365

if 0:
    input = [
    '...............',
    '..#..........#.',
    '...............',
    '..#..........#.',
    '...............',
    '...............',
    '...............',
    '.......S.......',
    '...............',
    '...............',
    '...............',
    '...............',
    '.#...........#.',
    '.##.........##.',
    '...............',
    ]

    oneside = 7
    steps = 7 + 15 * 6

side = oneside*2 + 1

for l in input:
    if 'S' in l:
        start = (l.index('S'), input.index(l))
        break

d = defaultdict(lambda: [1000000000, 1000000000000])


def cand1(pos):
    (x, y) = pos
    for (xd, yd) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        nx = x + xd
        ny = y + yd

        if nx < 0 or ny < 0 or nx >= len(input[0]) or ny >= len(input):
            continue
        yield(nx, ny, input[ny][nx])


def calc(pos, d, count, end, candgen):
    if count > end:
        return
    for (nx, ny, point) in candgen(pos):

        if point in ('.', 'S'):
            v = d[(nx, ny)]
            if v[count % 2] > count:
                v[count % 2] = count
                calc((nx, ny), d, count + 1, end, candgen)

d[start] = [0]

calc(start, d, 1, 64, cand1)

print("start:", d[start])

z = [x for x in d.values() if x[0] < 1000000000]

r1 = len(z)

print("r1:", r1)


def cand2(pos):

    (x, y) = pos
    for (xd, yd) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        nx = x + xd
        ny = y + yd

        point = input[ny % len(input)][nx % len(input[0])]

        yield(nx, ny, point)


def disp(d, mod2):

    field = defaultdict(lambda: '.')

    for (k, v) in [x for x in d.items() if x[1][mod2] < inf]:
        field[k] = 'O'

    minx = min([x[0] for x in field.keys()])
    maxx = max([x[0] for x in field.keys()])

    miny = min([x[1] for x in field.keys()])
    maxy = max([x[1] for x in field.keys()])

    print("-------------")
    for y in range(abs(maxy-miny)+1):
        str = ""
        for x in range(abs(maxx-minx)+1):
            str = str + field[(x+minx,y+miny)]
        print(str)

    print("-------------")
                

def skipped(start, mod2):

    # standard
    d = defaultdict(lambda: [inf, inf])
    d[start] = [0, inf]

    correction = 0 if mod2 else 1

    n = (oneside+1) // 2 - correction
    count = (n*(4 + 4*correction) + n * (n - 1) * (8 // 2)) + correction

    calc(start, d, 1, oneside, cand2)

    z = len([x for x in d.values() if x[mod2] < inf])

    print("zs:", z, count, count-z)

    standard = count - z

    #disp(d, mod2)

    # extra
    d = defaultdict(lambda: [inf, inf])
    d[start] = [0, inf]

    correction = 0 if mod2 else 1

    n = (oneside+1+2) // 2 - correction
    count = (n*(4 + 4*correction) + n * (n - 1) * (8 // 2)) + correction

    calc(start, d, 1, oneside+2, cand2)

    z = len([x for x in d.values() if x[mod2] < inf])

    print("ze:", z, count, count-z)

    extra = count - z

    disp(d, mod2)

    return (standard, extra)

    #zo = [x for x in d.values() if x[1] < inf]

#print("s:", skipped(start, 0))
#print("s:", skipped(start, 1))

(skippedO, _) = skipped(start, 1)
(_, skippedOprim) = skipped(start, 0)

#skippedOdd = skipped((side-1, 0), 0)
#skippedEven = skipped((side-1, 0), 1)
(_, skippedOdd) = skipped((side, 0), 1)
(_, skippedEven) = skipped((side, 0), 0)


print("s:", skipped(start, 1))
print("s:", skipped(start, 0))
print("s:", skipped((side, 0), 1))
print("s:", skipped((side, 0), 0))

n = (steps+1) // 2

total = (n*4 + n * (n - 1) * (8 // 2))

print("total:", total)

blocks = steps // side

print("blocks:", blocks)

halfside = blocks

# o prim
n = (blocks + 1) // 2
total -= (n*4 + n * (n - 1) * (8 // 2)) * skippedOprim

# o
n = blocks // 2
total -= ((n*8 + n * (n - 1) * (8 // 2)) + 1) * skippedO


# lisa 1 ja 2
n = blocks
total -= (n*4 + n * (n - 1) * (4 // 2)) * skippedOdd // 2
total -= (n*4 + n * (n - 1) * (4 // 2)) * skippedEven // 2


r2 = total


d = defaultdict(lambda: [inf, inf])
d[start] = [0, inf]

xx = 0
#calc(start, d, 1, steps, cand2)
#xx = len([x for x in d.values() if x[steps%2] < inf])

print("   ", 605899227785100)
print("r2:", r2)
print("xx:", xx)
print("   ", 627469647947433)

post.submit(total, part="b", day=21)
#627469647947433 too high

