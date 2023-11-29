
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

elements = list()

for l in input:
    (a, b) = tuple(map(int, l.split('/')))
    elements.append((a, b))


def find_candidates(free, elements, visited):
    for (e1, e2) in elements:
        if (e1 == free or e2 == free) and (e1, e2) not in visited:
            yield (e1, e2)

def calc(free, strength, depth, elements, visited):
    found = False
    for (e1, e2) in find_candidates(free, elements, visited):
        found = True
        c = (e1, e2)
        nextfree = e1 if free == e2 else e2
        for r in calc(nextfree, strength + e1 + e2, depth + 1, elements, visited.union((c,))):
            yield r

    if not found:
        yield (strength, depth)

r1 = 0
for (r, _) in calc(0, 0, 0, elements, set()):
    r1 = max(r1, r)

post.submit(r1, part="a", day=24, year=2017)

r2 = 0
d2 = 0
for (r, d) in calc(0, 0, 0, elements, set()):
    if d >= d2:
        r2 = max(r2, r)
        d2 = d

post.submit(r2, part="b", day=24, year=2017)
