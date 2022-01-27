
from datetime import datetime

t1 = datetime.now()

text_file = open("input09.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

yd = len(lines)
xd = len(lines[0])

field = {}
for y in range(yd):
    for x in range(xd):
        field[(x,y)] = int(lines[y][x])

def uppers(x,y):
    v = field[(x,y)]
    u = []

    out = 0
    if x > 0:
        if field[(x-1, y)] > v:
            u.append((x-1, y))
    else:
        out += 1

    if y > 0:
        if field[(x, y-1)] > v:
            u.append((x, y-1))
    else:
        out += 1

    if x < xd-1:
        if field[(x+1, y)] > v:
            u.append((x+1, y))
    else:
        out += 1

    if y < yd-1:
        if field[(x, y+1)] > v:
            u.append((x, y+1))
    else:
        out += 1

    return (u, out)

def low(x, y):
    (u, out) = uppers(x,y)

    return len(u) + out == 4

score = 0
basins = []
for ((x,y), v) in field.items():
    if low(x,y):
        score += 1 + v
        basins.append((x,y))

print("Part1:", score)

bsizes = []

for b in basins:
    q = set([b])
    visited = set()
    while len(q) > 0:
        (x,y) = q.pop()
        visited.add((x,y))
        (u, out) = uppers(x, y)
        u = filter(lambda x: field[(x[0], x[1])] < 9, u)
        q = q.union(u).difference(visited)

    bsizes.append(len(visited))

a = list(reversed(sorted(bsizes)))

print("Part2:", a[0]*a[1]*a[2])
