
from collections import defaultdict
from datetime import datetime

tstart = datetime.now()

text_file = open("input05.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def genpoints(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        if x1 > x2:
            (x1, x2) = (x2, x1)
        if y1 > y2:
            (y1, y2) = (y2, y1)

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                yield (x, y)
    else:
        if (x1 > x2 and y1 < y2) or (x1 < x2 and y1 > y2):
            if x1 > x2:
                y1 = y2
                (x1, x2) = (x2, x1)
            cy = -1
        else:
            (x1, x2) = (min(x1, x2), max(x1, x2))
            (y1, y2) = (min(y1, y2), max(y1, y2))
            cy = 1
        for z in range((x2-x1)+1):
            yield (x1+z, y1+cy*z)

counts1 = defaultdict(int)
counts2 = defaultdict(int)

for l in lines:
    (p1, a, p2) = l.split(' ')
    (x1, y1) = tuple(map(int, p1.split(',')))
    (x2, y2) = tuple(map(int, p2.split(',')))

    s = genpoints(x1, y1, x2, y2)
    if x1 == x2 or y1 == y2:
        for p in s:
            counts1[p] += 1
            counts2[p] += 1
    else:
        for p in s:
            counts2[p] += 1

print("Part1: ", len(tuple(filter(lambda x: x > 1, counts1.values()))))

print("Part2: ", len(tuple(filter(lambda x: x > 1, counts2.values()))))

print("Time:", (datetime.now() - tstart).microseconds // 1000)
