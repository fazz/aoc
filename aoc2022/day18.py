
import datetime
from copy import deepcopy, copy
from itertools import product
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

particles = {tuple(map(int, x.rstrip(" \n\r").split(','))) for x in open("input18.txt", "r")}

(maxx, maxy, maxz) = (0, 0, 0)

def calc(particles):
    global maxx, maxy, maxz

    sidec = defaultdict(int)

    for p in particles:
        (x, y, z) = p

        (maxx, maxy, maxz) = (max(maxx, x), max(maxy, y), max(maxy, z))

        sidec[('b', x,y,z)] += 1
        sidec[('b', x,y,z+1)] += 1

        sidec[('f', x,y,z)] += 1
        sidec[('f', x,y+1,z)] += 1

        sidec[('s', x,y,z)] += 1
        sidec[('s', x+1,y,z)] += 1

    return sum([x for x in sidec.values() if x == 1])

print("Part 1:", calc(particles))

interesting = set(product(range(maxx+2), range(maxy+2), range(maxz+2))).difference(particles)

dist = {i: 999999 for i in interesting}
dist[(0,0,0)] = 0

q = PriorityQueue()

for d in dist.items():
    q.put((d[1], d[0]))

while q.qsize() > 0:
    u = q.get()

    (x,y,z) = u[1]

    paths = set([(x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z), (x,y,z+1), (x,y,z-1)]).difference(particles)
    
    for v in paths:
        if v not in dist:
            continue
        alt = dist[u[1]] + 1
        if alt < dist[v]:
            dist[v] = alt
            q.put((alt, v))

trapped = [x[0] for x in dist.items() if x[1] == 999999]

print("Part 2:", calc(particles.union(trapped)))

end = datetime.datetime.now()

print("Milliseconds:", (end-start_time).seconds*1000 + (end-start_time).microseconds // 1000)
