
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

r1 = 0
r2 = 0

limits = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def parse(g):
    (pr, d) = g.split(': ')
    trials = d.split('; ')
    (_, n) = pr.split(' ')

    n = int(n)

    rt = []

    for t in trials:
        rt.append(map(lambda v: (int(v[0]), v[1]), [vv.split(' ') for vv in t.split(', ')]))

    return (n, rt)

for g in input:

    lowest = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    possible = True

    (n, trials) = parse(g)
    for trial in trials:
        for (count, color) in trial:
            if count > limits[color]:
                possible = False
            lowest[color] = max(lowest[color], count)

    if possible:
        r1 = r1 + n

    power = lowest['green']*lowest['red']*lowest['blue']

    r2 += power

post.submit(r1, part="a", day=2)
post.submit(r2, part="b", day=2)
