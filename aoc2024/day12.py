
from aocd import data, post

input = data.split('\n')

def inside(x, y, matrix):
    return y >= 0 and x >= 0 and y < len(matrix) and x < len(matrix[0])

def getgroup(x,y):
    ret = set()
    v = input[y][x]
    next = set([(x,y),])
    outside = 0
    while len(next) > 0:
        p = next.pop()
        ret.add(p)
        (x,y) = p
        for (dx,dy) in ((0,1), (1,0), (-1,0), (0,-1)):
            nx = x + dx
            ny = y + dy
            if inside(nx, ny, input) and input[ny][nx] == v and (nx,ny) not in ret:
                next.add((nx,ny))
            if (not inside(nx, ny, input)) or input[ny][nx] != v:
                outside += 1

    return (ret, outside)

def getsides(gr):
    sides = 0
    for p in gr:
        d = (1,0)
        outd = set()
        cout = (p[0]+d[0], p[1]+d[1]) not in gr
        for _ in range(4):
            d = (-d[1], d[0])
            nout = (p[0]+d[0], p[1]+d[1]) not in gr
            if nout:
                outd.add(d)
                if cout and (p[0]+d[0]+d[1], p[1]+d[1]-d[0]) not in gr:
                    sides += 1
            cout = nout

        for ld in outd:
            if (p[0]+ld[0]+ld[1], p[1]+ld[1]-ld[0]) in gr:
                sides += 1
    return sides

r1 = 0
r2 = 0

visited = set()

for y in range(len(input)):
    for x in range(len(input[0])):
        if (x,y) in visited:
            continue
        (gr, fl) = getgroup(x, y)

        r1 += fl*len(gr)

        r2 += getsides(gr)*len(gr)

        visited = visited.union(gr)

post.submit(r1, part="a", day=12)
post.submit(r2, part="b", day=12)
