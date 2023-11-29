
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

xinput = [
'..#',
'#..',
'...',
]

px = py = len(input[0])//2
d = (0, -1)

field = {}

for li in range(len(input)):
    if li not in field:
        field[li] = defaultdict(lambda: '.')
    for ci in range(len(input[li])):
        c = input[li][ci]
        field[li][ci] = c

r1 = 0

for zz in range(10000):
    if py not in field:
        field[py] = defaultdict(lambda: '.')

    v = field[py][px]
    if v == '.':
        d = (d[1], -d[0])
        nv = '#'
        r1 += 1
    else:
        d = (-d[1], d[0])
        nv = '.'

    field[py][px] = nv
    (px, py) = (px + d[0], py + d[1])

post.submit(r1, part="a", day=22, year=2017)

###

px = py = len(input[0])//2
d = (0, -1)

field = {}

for li in range(len(input)):
    if li not in field:
        field[li] = defaultdict(lambda: '.')
    for ci in range(len(input[li])):
        c = input[li][ci]
        field[li][ci] = c

r2 = 0

for zz in range(10000000):
    if py not in field:
        field[py] = defaultdict(lambda: '.')

    v = field[py][px]
    if v == '.':
        d = (d[1], -d[0])
        nv = 'W'
    elif v == 'W':
        nv = '#'
        r2 += 1
    elif v == '#':
        d = (-d[1], d[0])
        nv = 'F'
    else:
        d = (-d[0], -d[1])
        nv = '.'

    field[py][px] = nv
    (px, py) = (px + d[0], py + d[1])

post.submit(r2, part="b", day=22, year=2017)

