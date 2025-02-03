
from aocd import data, post

from aoc import inside, inside2, uniform_cost_search, astar

input = data.split('\n')


input = [[int(c) for c in l] for l in input]

end = (len(input[0])-1, len(input)-1)

def neighbors_simple(node):
    (x, y) = node
    for (dx, dy) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        nx = x + dx
        ny = y + dy

        if not inside(nx, ny, input):
            continue
        yield (input[ny][nx], (nx, ny))

shortest = uniform_cost_search(end, neighbors_simple)

def h(node):
    return shortest[(node[0], node[1])]

def neighbors_internal(node, l, h, precalc):
    node = (node[0], node[1], abs(node[2]), abs(node[3]))
    (x, y, dx, dy) = node

    if node in precalc:
        return precalc[node]
    
    r = []
    for _ in range(2):
        d = 0
        nx = x + dx
        ny = y + dy
        for s in range(1, l):
            if not inside2(nx, ny, end[0], end[1]):
                break
            d += input[ny][nx]
            nx += dx
            ny += dy
        for _ in range(l, h+1):
            if not inside2(nx, ny, end[0], end[1]):
                break
            d += input[ny][nx]
            r.append((d, (nx, ny, dy, -dx)))
            nx += dx
            ny += dy
        dx = -dx
        dy = -dy
    precalc[node] = r
    return r

nbprecalc1 = {}
def neighbors1(node):
    return neighbors_internal(node, 1, 3, nbprecalc1)

nbprecalc2 = {}
def neighbors2(node):
    return neighbors_internal(node, 4, 10, nbprecalc2)

def verifygoal(node):
    node = (node[0], node[1])
    return end == node

(r1, p1) = astar((0, 0, 1, 0), verifygoal, neighbors1, h)
print("r1:", r1)
post.submit(r1, part="a", day=17)

(r2, p2) = astar((0, 0, 1, 0), verifygoal, neighbors2, h)
print("r2:", r2)

post.submit(r2, part="b", day=17)
