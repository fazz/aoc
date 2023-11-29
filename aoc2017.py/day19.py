
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re

input = data.split('\n')

p = (input[0].index('|'), 0)
d = (0, 1)

r1 = []
r2 = 0

while True:
    p = (p[0] + d[0], p[1] + d[1])
    r2 += 1
    c = input[p[1]][p[0]]
    if c == ' ':
        break
    elif c in ('-', '|'):
        continue
    elif 'A' <= c <= 'Z':
        r1.append(c)
        continue
    elif c == '+':
        d = (d[1], -d[0])
        c2 = input[p[1] + d[1]][p[0] + d[0]]
        if c2 in ('-', '|'):
            continue
        d = (-d[0], -d[1])

r1 = ''.join(r1)

post.submit(r1, part="a", day=19, year=2017)

post.submit(r2, part="b", day=19, year=2017)
