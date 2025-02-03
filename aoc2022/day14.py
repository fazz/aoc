
from copy import deepcopy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict

lines = [x.rstrip(" \n\r") for x in open("input14.txt", "r")]

cave = defaultdict(lambda: defaultdict(int))

lowestpoint = 0

for l in lines:
    ls = [x.rstrip(' >').lstrip(' >') for x in l.split('-')]

    (x1, y1) = map(int, ls.pop(0).split(','))
    while len(ls) > 0:

        (x2, y2) = map(int, ls[0].split(','))

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                cave[y][x1] = 1
        else:
            for x in range(min(x1, x2), max(x1, x2)+1):
                cave[y1][x] = 1

        lowestpoint = max(lowestpoint, y1)
        lowestpoint = max(lowestpoint, y2)

        (x1, y1) = map(int, ls.pop(0).split(','))
    
def calc(cave, extrasupport):
    count = 0
    stop = False

    (x,y) = (500, 0)

    while not stop:
        if (x,y) == (500, 0):
            count += 1

        if extrasupport and y == lowestpoint +1:
            cave[y][x] = 2
            (x,y) = (500, 0)
            continue

        if cave[y+1][x] == 0:
            y += 1
        elif cave[y+1][x-1] == 0:
            x -= 1
            y += 1
        elif cave[y+1][x+1] == 0:
            x += 1
            y += 1
        else:
            cave[y][x] = 2
            if (x,y) == (500, 0):
                stop = True

            (x,y) = (500, 0)

        if y == lowestpoint + 2:
            count -= 1
            stop = True
            continue

    return count

print("Part 1:", calc(deepcopy(cave), False))

print("Part 2:", calc(cave, True))
