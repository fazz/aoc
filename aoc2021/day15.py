
from datetime import datetime
from collections import defaultdict

t1 = datetime.now()

text_file = open("input15.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

dim = len(lines)

field = []
for y in range(dim):
    field.append([])
    for x in range(dim):
        field[y].append(int(lines[y][x]))

def get(k):
    (x,y) = k
    xc = x // dim
    x = x % dim
    yc = y // dim
    y = y % dim
    return ((field[y][x] + xc + yc - 1) % 9) + 1

def nexts(p,m,q):
    (x,y) = p
    u = set()

    if x > 0:
        u.add((x-1, y))

    if y > 0:
        u.add((x, y-1))

    if x < dim*m-1:
        u.add((x+1, y))

    if y < dim*m-1:
        u.add((x, y+1))

    return u.intersection(q)

m=5

dist = defaultdict(lambda: (dim+dim)*10*m)
distmap = defaultdict(set)
dist[(0,0)] = 0
distmap[0] = set([(0,0)])

q = {(x,y) for x in range(100*m) for y in range(100*m)}

while len(q) > 0:
    pos = distmap[min(distmap)].pop()
    if len(distmap[min(distmap)]) == 0:
        del distmap[min(distmap)]
    if pos not in q:
        continue
    q.remove(pos)

    nx = nexts(pos,m,q)

    for n in nx:
        alt = dist[pos] + get(n)
        if alt < dist[n]:
            dist[n] = alt
            distmap[alt].add(n)

print("Part1:", dist[(99,99)])
print("Part2:", dist[(499,499)])
