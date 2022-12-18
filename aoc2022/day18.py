import datetime
from copy import deepcopy, copy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

lines = [x.rstrip(" \n\r") for x in open("input18.txt", "r")]

result1 = 0

sidec = defaultdict(int)

maxx = 0
maxy = 0
maxz = 0

cubes = set()

for l in lines:
    (x, y, z) = [int(x) for x in l.split(',')]
    maxx = max(maxx, x)
    maxy = max(maxy, y)
    maxz = max(maxy, z)
    cubes.add((x,y,z))

    sidec[('b', x,y,z)] += 1
    sidec[('b', x,y,z+1)] += 1

    sidec[('f', x,y,z)] += 1
    sidec[('f', x,y+1,z)] += 1

    sidec[('s', x,y,z)] += 1
    sidec[('s', x+1,y,z)] += 1

result1 = sum([x for x in sidec.values() if x == 1])

print("Part 1:", result1)

interesting = []

for a in range(maxx+2):
    for b in range(maxy+2):
        for c in range(maxz+2):
            if (a,b,c) not in cubes:
                interesting.append((a,b,c))

dist = {i: 999999 for i in interesting}
dist[(0,0,0)] = 0

q = PriorityQueue()

for d in dist.items():
    q.put((d[1], d[0]))

while q.qsize() > 0:
    u = q.get()

    (x,y,z) = u[1]

    paths = set([(x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z), (x,y,z+1), (x,y,z-1)]).difference(cubes)
    
    for v in paths:
        if v not in dist:
            continue
        alt = dist[u[1]] + 1
        if alt < dist[v]:
            dist[v] = alt
            q.put((alt, v))

trapped = [x[0] for x in dist.items() if x[1] == 999999]

result2 = result1

for t in trapped:
#    print(trapped)
    (x,y,z) = t
    if ('b', x,y,z) in sidec:
        sidec[('b', x,y,z)] += 1
    if ('b', x,y,z+1) in sidec:
        sidec[('b', x,y,z+1)] += 1

    if ('f', x,y,z) in sidec:
        sidec[('f', x,y,z)] += 1
    if ('f', x,y+1,z) in sidec:
        sidec[('f', x,y+1,z)] += 1

    if ('s', x,y,z) in sidec:
        sidec[('s', x,y,z)] += 1

    if ('s', x+1,y,z) in sidec:
        sidec[('s', x+1,y,z)] += 1
    
result2 = sum([x for x in sidec.values() if x == 1])

print("Part 2:", result2)
# 3495 vale

end = datetime.datetime.now()

print("Milliseconds:", (end-start_time).seconds*1000 + (end-start_time).microseconds // 1000)

