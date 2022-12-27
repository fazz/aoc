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

lines = [x.rstrip(" \n\r") for x in open("input22.txt", "r")]

field = defaultdict(lambda: defaultdict(lambda: ' '))

pairs1 = {}
startx = None

for li in range(0, len(lines)-2):
    l = lines[li]

    fc = None

    for ci in range(len(l)):
        c = l[ci]
        field[ci+1][li+1] = c
        if c in ('.', '#'):
            if fc == None:
                fc = ci+1
        if startx == None and c == '.' and li == 0:
            startx = ci+1

    pairs1[(fc, li+1, (-1, 0))] = (len(l), li+1, (-1, 0))
    pairs1[(len(l), li+1, (1, 0))] = (fc, li+1, (1, 0))

guide = ['']

for c in lines[-1]:
    if c in ('R', 'L'):
        guide.append(int(guide.pop()))
        guide += [c, '']
    else:
        guide[-1] += c
guide.append(int(guide.pop()))        

for x in field:
    y1 = min([y for y in field[x] if field[x][y] != ' ' ])
    y2 = max([y for y in field[x] if field[x][y] != ' ' ])

    pairs1[(x, y1, (0, -1))] = (x, y2, (0, -1))
    pairs1[(x, y2, (0, 1))] = (x, y1, (0, 1))

def wrap(nose, x, y, pairs):
    (nx, ny, nnose) = pairs[(x,y,nose)]
    if field[nx][ny] == '.':
        return (nx, ny, nnose)
    return (x, y, nose)

def calc(x, y, pairs):

    nose = (1, 0)

    for g in guide:
        if isinstance(g, int):
            for _ in range(g):
                nx = x + nose[0]
                ny = y + nose[1]
                if field[nx][ny] == '#':
                    break
                elif field[nx][ny] == ' ':
                    (x, y, nose) = wrap(nose, x, y, pairs)
                else:
                    (x, y) = (nx, ny)
        else:
            if g == 'R':
                nose = (-nose[1], nose[0])
            else:
                nose = (nose[1], -nose[0])

    dc = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}

    return 1000*y + 4*x + dc[nose]

print("Part 1:", calc(startx, 1, pairs1), 189140)

sz = 50

starters = []

corners = {
    0: (1, 0, 0, -1, 0, 1, -1, 0),
    3: (0, 1, 0, 1, 1, 0, 1, 0)
}

for x in range(4):
    x = (x+1)*50
    for y in range(4):
        y = (y+1)*50

        cells = []
        for ax in range(2):
            for ay in range(2):
                cells.append(field[x+ax][y+ay])
        if len(tuple(filter(lambda x: x == ' ', cells))) != 1:
            continue

        c = corners[cells.index(' ')]
        starters.append( ((x+c[0], y+c[1]), (c[2], c[3]), (c[3], -c[2]) ) )
        starters.append( ((x+c[4], y+c[5]), (c[6], c[7]), (-c[7], c[6]) ) )

pairs2 = {}

def nxt(x, y, nose, wd):
    nx = x + nose[0]
    ny = y + nose[1]

    if field[nx][ny] == ' ':
        for (nnose, nwd) in (((-nose[1], nose[0]), (-wd[1], wd[0])), ((nose[1], -nose[0]), (wd[1], -wd[0]))):
            nx = x + nnose[0]
            ny = y + nnose[1]
            if field[nx][ny] != ' ':
                return (x, y, nnose, nwd)

    if field[nx-nose[1]][ny+nose[0]] != ' ' and field[nx+nose[1]][ny-nose[0]] != ' ':
        if field[nx-nose[1]-nose[0]][ny+nose[0]-nose[1]] == ' ':
            return (nx-nose[1], ny+nose[0], (-nose[1], nose[0]), (-wd[1], wd[0]))

        if field[nx+nose[1]-nose[0]][ny-nose[0]-nose[1]] == ' ':
            return (nx+nose[1], ny-nose[0], (nose[1], -nose[0]), (wd[1], -wd[0]))

    return (nx, ny, nose, wd)

while len(pairs2) < sz*7*2:

    ((x1, y1), nose1, wd1) = starters.pop(0)
    ((x2, y2), nose2, wd2) = starters.pop(0)

    while True:
        pairs2[(x1, y1, wd1)] = (x2, y2, (-wd2[0], -wd2[1]))
        pairs2[(x2, y2, wd2)] = (x1, y1, (-wd1[0], -wd1[1]))

        (x1, y1, nnose1, wd1) = nxt(x1, y1, nose1, wd1)
        (x2, y2, nnose2, wd2) = nxt(x2, y2, nose2, wd2)

        if nnose1 != nose1 and nnose2 != nose2:
            break
        nose1 = nnose1
        nose2 = nnose2

print("Part 2:", calc(startx, 1, pairs2), 115063)
