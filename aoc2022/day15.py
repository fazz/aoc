
import datetime
from copy import deepcopy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

start_time = datetime.datetime.now()

lines = [x.rstrip(" \n\r") for x in open("input15.txt", "r")]

line  = 2000000
limit = 4000000

sensors = {}
beacons = set()

for l in lines:
    g = re.search('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)', l)
    (sx,sy,bx,by) = map(int, (g.groups()[0:4]))

    dist = abs(bx-sx) + abs(by-sy)

    sensors[(sx,sy)] = dist
    beacons.add((bx,by))

def linenobeacons(line):
    segments = []
    for s in sensors.items():
        x = s[0][0]
        y = s[0][1]
        d = s[1]

        if (y >= line and y-d <= line) or (y <= line and y+d >= line):
            leftover = d - abs(y-line)
            segments.append((x-leftover, x+leftover))

    segments = sorted(segments, key=lambda x: x[0])

    i = 0
    while i < len(segments)-1:
        if segments[i+1][0] <= segments[i][1]:
            v1 = segments.pop(0)
            v2 = segments.pop(0)
            segments.insert(0, (min(v1[0], v2[0]), max(v1[1], v2[1])))
        else:
            i += 1

    count = sum([x[1]-x[0]+1 for x in segments])
    return count

count = linenobeacons(line)

bonline = len(list(filter(lambda x: x[1] == line, beacons)))

print("Part 1:", count-bonline)

borders = set()

for s in sensors.items():
    x = s[0][0]
    y = s[0][1]
    d = s[1]+1

    borders.add(((x-d, y), (x, y+d)))
    borders.add(((x, y+d), (x+d, y)))
    borders.add(((x+d, y), (x, y-d)))
    borders.add(((x, y-d), (x-d, y)))

candidates = set()

ccount = 0
while len(borders) > 0:
    b = borders.pop()
    for b2 in borders:
        # There is a curious property:
        # undetected beacons can reside only in places
        # where at least two outer borders of a sensor area intersect.
        (has_intersect, collinear, data) = intersect(b, b2)
        if has_intersect and not collinear:
            (x,y) = data
            if x >= 0 and y >= 0 and x <= limit and y <= limit:
                candidates.add(data)
            ccount += 1

(x,y) = (0,0)
while True:
    (x,y) = candidates.pop()
    mismatch = False
    for s in sensors.items():
        sx = s[0][0]
        sy = s[0][1]
        d = s[1]

        dd = abs(x-sx)+abs(y-sy)
        if dd <= d:
            mismatch = True
            break
    if mismatch:
        continue

    break

print("Part 2:", x*4000000+y)

end = datetime.datetime.now()

print("Milliseconds:", (end-start_time).seconds*1000 + (end-start_time).microseconds // 1000)
