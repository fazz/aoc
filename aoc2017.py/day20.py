
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import math
from itertools import chain, product

input = data.split('\n')

count = 3000

dists = {}

parts = []

for li in range(len(input)):
    l = input[li]
    s = l.split(', ')
    p = tuple(map(int, s[0][3:-1].split(',')))
    v = tuple(map(int, s[1][3:-1].split(',')))
    a = tuple(map(int, s[2][3:-1].split(',')))

    parts.append((p, v, a))

    z = lambda x: p[x] + count*v[x] + (count*a[x])+((count)*(count-1)*a[x])//2
    p = (z(0), z(1), z(2))

    p = (p[0] + count*v[0] + (count//2)*(count-1)*a[0], p[1] + count*v[1] + (count//2)*(count-1)*a[1], p[2] + count*v[2] + (count//2)*(count-1)*a[2])

    dist = abs(p[0]) + abs(p[1]) + abs(p[2])

    dists[li] = dist
    
r1 = sorted(dists.items(), key=lambda x: x[1])[0][0]

post.submit(r1, part="a", day=20, year=2017)

###

def solve(i, j, coord):
    a = (parts[i][2][coord] - parts[j][2][coord]) / 2
    b = a + parts[i][1][coord] - parts[j][1][coord]
    c = parts[i][0][coord] - parts[j][0][coord]

    if a == 0:
        if b == 0:
            if c == 0:
                return (True, [None])
            return (False, -1)
        s = -c / b
        if int(s) != s:
            return (False, -1)
        return (True, [int(s)])

    sr = b*b - 4 * a *c
    if sr < 0:
        return (False, -1)
    sr = math.sqrt(sr)

    u = tuple(map(int, filter(lambda x: x >= 0 and int(x) == x, [(-b + sr) / (2*a), (-b - sr) / (2*a)])))

    if len(u) == 0:
        return (False, -1)
 
    return (True, u)

coll = defaultdict(lambda: defaultdict(set))
for i in range(len(input)-1):
    for j in range(i+1, len(input)):
        (tx, sx) = solve(i, j, 0)
        (ty, sy) = solve(i, j, 1)
        (tz, sz) = solve(i, j, 2)
        if not (tx and ty and tz):
            continue

        bad = True
        for v in product(sx, sy, sz):
            values = set(filter(lambda x: x is not None, v))

            step = 0
            if len(set(values)) == 0:
                bad = False
            elif len(set(values)) == 1:
                bad = False
                step = values.pop()
            elif len(set(values)) >= 1:
                continue
        if bad:
            continue

        coll[step][i].add(j)
        coll[step][j].add(i)

killed = set()
for t in sorted(coll.keys()):
    for p in set(coll[t].keys()).difference(killed):
        killed.add(p)
        for p2 in coll[t][p].difference(killed):
            killed.add(p2)

r2 = len(input) - len(killed)

post.submit(r2, part="b", day=20, year=2017)
