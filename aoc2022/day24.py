import datetime
from copy import deepcopy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

lines = [x.rstrip(" \n\r") for x in open("input24.txt", "r")]

(miny, maxy, mix, maxx) = (1, len(lines)-2, 1, len(lines[0])-2)

start_pos = (lines[0].index('.'), miny-1)
end_pos = (lines[-1].index('.'), maxy+1)

bd = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}

blizzards = set()

for li in range(len(lines)):
    for ci in range(len(lines[li])):
        if lines[li][ci] not in ('.', '#'):
            blizzards.add((ci, li, *(bd[lines[li][ci]])))

blizzardminute = {0: {(z[0], z[1]) for z in blizzards}}

def updateblizzard(minute):
    p = max(blizzardminute)

    for m in range(p+1, minute+1):
        ns = set()
        blizzardminute[m] = ns
        for b in blizzards:
            ns.add(((b[0]+b[2]*m-1)%maxx+1, (b[1]+b[3]*m-1)%maxy+1))

def getdirections(minute, x, y):
    if minute not in blizzardminute:
        updateblizzard(minute)
    bzrds = blizzardminute[minute]

    ret = []
    for (xd, yd) in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
        (nx, ny) = (x+xd, y+yd)
        if (nx >= 1 and nx <= maxx and ny >= 1 and ny <= maxy and (nx, ny) not in bzrds) or (nx, ny) == end_pos or (nx, ny) == start_pos:
            ret.append((minute, nx, ny))

    return ret

q = PriorityQueue()

visited = set([(0, *start_pos)])

q.put((0, *start_pos))

result1 = None
result2 = None
targets = [end_pos, start_pos, end_pos]

while q.qsize() > 0:
    curr = q.get()

    (minute, x, y) = curr

    if (x,y) == targets[0]:
        targets.pop(0)
        if result1 == None:
            result1 = minute
        if len(targets) == 0:
            result2 = minute
            break
        q = PriorityQueue()
        visited = set(curr)

    free = getdirections(minute+1, x, y)

    for step in free:
        if step not in visited:
            visited.add(step)
            q.put(step)

print("Part 1:", result1)
print("Part 2:", result2)
