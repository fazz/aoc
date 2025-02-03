
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter, deque
from itertools import chain
from queue import PriorityQueue
from math import inf, sqrt
from copy import copy
import operator
import re
import sys
import sympy as sp
from sympy.solvers import solve

from aoc import raycross2D

input = data.split('\n')

stones = set()

for l in input:
    (p, s) = l.split(' @ ')
    p = tuple(map(int, p.split(', ')))
    s = tuple(map(int, s.split(', ')))

    stones.add((p, s))

r1 = 0

visited = set()
for s1 in stones:
    visited.add(s1)
    ((px1, py1, pz1), (sx1, sy1, sz1)) = s1
    for s2 in stones.difference(visited):

        x = raycross2D((s1[0][:2], s1[1][:2]),(s2[0][:2],s2[1][:2]))

        if x is not None:
            (ex, ey) = x
            if 200000000000000 <= ex <= 400000000000000 and 200000000000000 <= ey <= 400000000000000:
                r1 += 1

print("r1:", r1)

post.submit(r1, part="a", day=24)

(rx, ry, rz, rvx, rvy, rvz) = sp.symbols('rx, ry, rz, rvx, rvy, rvz')

eqs = list()

((x1,y1,z1), (vx1, vy1, vz1)) = stones.pop()

(pvx1, pvy1, pvz1) = (rx - x1, ry - y1, rz - z1)
(vvx1, vvy1, vvz1) = (rvx - vx1, rvy - vy1, rvz - vz1)

for i in range(2):
    ((x2,y2,z2), (vx2, vy2, vz2)) = stones.pop()

    (pvx2, pvy2, pvz2) = (rx - x2, ry - y2, rz - z2)

    (vvx2, vvy2, vvz2) = (rvx - vx2, rvy - vy2, rvz - vz2)

    eqs.append(sp.Eq(pvy2*vvz2 - vvy2*pvz2, pvy1*vvz1 - vvy1*pvz1))
    eqs.append(sp.Eq(pvz2*vvx2 - vvz2*pvx2, pvz1*vvx1 - vvz1*pvx1))
    eqs.append(sp.Eq(pvx2*vvy2 - vvx2*pvy2, pvx1*vvy1 - vvx1*pvy1))

output = solve(eqs,dict=True)[0]

r2 = int(output[rx]+output[ry]+output[rz])

print("r2:", r2)

post.submit(r2, part="b", day=24)

#https://old.reddit.com/r/adventofcode/comments/18pnycy/2023_day_24_solutions/kepu26z/
#https://www.reddit.com/r/adventofcode/comments/18q7d47/2023_day_24_part_2_a_mathematical_technique_for/
