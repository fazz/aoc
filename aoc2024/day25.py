
import sys
sys.path.insert(0, "../aoc2023")

from aocd import data, post
from itertools import product

from aoc import transposestringmatrix, filtersplit

input = map(lambda x: x.split('\n'), data.split('\n\n'))

(lit, kit) = filtersplit(lambda x: x[0] == '#####', input)

locks = [[x.count('#') for x in transposestringmatrix(lock)] for lock in lit]
keys = [[x.count('#') for x in transposestringmatrix(key)] for key in kit]

r1 = 0
for x in product(locks, keys):
    if max(map(sum, zip(*x))) < 8:
        r1 += 1

post.submit(r1, part="a", day=25)
