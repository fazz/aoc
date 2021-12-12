
from copy import copy

text_file = open("input11.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

xdim = len(lines[0])
ydim = len(lines)

def change(cells):
    tobeincreased = list(cells.keys())
    while len(tobeincreased) > 0:
        tbi = tobeincreased.pop()
        pv = cells[tbi]
        cells[tbi] += 1
        if pv ==  9:
            (x,y) = tbi
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == dy == 0:
                        continue
                    z = (x+dx, y+dy)
                    if z in cells:
                        tobeincreased.append(z)
    c = len(list(filter(lambda e: e > 9, cells.values())))
    cells = {k:v for (k, v) in map(lambda e: (e[0], 0 if e[1] > 9 else e[1]), cells.items())}
    return (cells, c)

cells = {}

for y in range(ydim):
    for x in range(xdim):
        cells[(x,y)] = int(lines[y][x])

ocells = copy(cells)

cycles = 100
count = 0

for c in range(cycles):
    (cells, c) = change(cells)
    count += c

print("Part1:", count)

cells = ocells

count = 0
rnd = 0

while count != xdim*ydim:
    (cells, count) = change(cells)
    rnd += 1

print("Part2:", rnd)

