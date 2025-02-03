
import sys
sys.path.insert(0, "../aoc2023")

from aocd import data, post

from aoc import uniform_cost_search, inside

input = data.split('\n')

start = None
end = None

for j, _ in enumerate(input):
    for i, v in enumerate(input[j]):
        if v == 'S':
            start = (i,j)
        if v == 'E':
            end = (i,j)
    if start is not None and end is not None:
        break

def neighbors(node):
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        (nx, ny) = (node[0]+d[0], node[1]+d[1])
        if input[ny][nx] in ('.', 'S', 'E'):
            yield (1, (nx, ny))

expanded = uniform_cost_search(start, neighbors)

fullcost = expanded[end]

path = [x for x in expanded.keys()]

saving=100

r1 = 0
r2 = 0

def generatemanhattan(p, dist):
    (x,y) = p
    for invoffset, offset in [(dist - x, x) for x in range(dist)]:
        yield ((x + offset, y + invoffset))
        yield ((x + invoffset, y - offset))
        yield ((x - offset, y - invoffset))
        yield ((x - invoffset, y + offset))

for cp in range(len(path)-saving-2):
    cheatpoint = path[cp]

    for dist in range(2, 21):
        for np in generatemanhattan(cheatpoint, dist):
            if not inside(*np, input):
                continue
            if input[np[1]][np[0]] not in ('.', 'S', 'E'):
                continue
            
            z =  expanded[np] - expanded[cheatpoint]
            if dist == 2:
                if z - 2 >= saving:
                    r1 += 1

            if z - dist >= saving:
                r2 += 1

print("r1:", r1)
print("r2:", r2)

post.submit(r1, part="a", day=20)
post.submit(r2, part="b", day=20)
