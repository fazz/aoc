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

lines = [x.rstrip(" \n\r") for x in open("input23.txt", "r")]

inputelves = set()

for li in range(len(lines)):
    for ci in range(len(lines[li])):

        if lines[li][ci] == '#':
            inputelves.add((ci, li))

inputcheckorder = []
inputcheckorder.append(((0, -1), (-1, -1), (1, -1)))
inputcheckorder.append(((0, 1), (-1, 1), (1, 1)))
inputcheckorder.append(((-1, 0), (-1, 1), (-1, -1)))
inputcheckorder.append(((1, 0), (1, 1), (1, -1)))

def calc(elves: set, checkorder: list):
    moveto = defaultdict(list)
    changed = False
    
    for e in elves:
        (x, y) = e

        movableto = None
        movecount = 0
        for c in checkorder:
            if not ((x+c[0][0], y+c[0][1]) in elves or (x+c[1][0], y+c[1][1]) in elves or (x+c[2][0], y+c[2][1]) in elves):
                movecount += 1
                if movableto == None:
                    movableto = (x+c[0][0], y+c[0][1])

        if movecount >= 1 and movecount <= 3:
            moveto[movableto].append((x,y))

    for (m, s) in moveto.items():
        if len(s) > 1:
            continue
        elves.remove(s[0])
        elves.add(m)
        changed = True

    checkorder.append(checkorder.pop(0))
    return (elves, changed, checkorder)

co = deepcopy(inputcheckorder)
elves = deepcopy(inputelves)
for _ in range(10):
    (elves, _, co) = calc(elves, co)

result1 = 0

for x in range(min([e[0] for e in elves]), max([e[0] for e in elves])+1):
    for y in range(min([e[1] for e in elves]), max([e[1] for e in elves])+1):
        result1 += 1 if (x,y) not in elves else 0

print("Part 1:", result1, 4138)

round = 11
while True:
    (ne, changed, co) = calc(elves, co)
    if not changed:
        break
    elves = ne
    round += 1

print("Part 2:", round, 1010)
