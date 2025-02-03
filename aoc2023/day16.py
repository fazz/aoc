
from aocd import data, post
from operator import xor

from aoc import inside, faceinside

input = data.split('\n')

precalc = {}

def energize(v):
    global precalc
    r = []
    n = []

    (x,y,xd,yd) = v

    r.append((x,y))

    if input[y][x] in ('|', '-') and xor(xd != 0, input[y][x] == '-'):
        (r, n) = energize((x, y, yd, -xd))
        (r2, n2) = energize((x, y, -yd, xd))

        r.extend(r2)
        n.extend(n2)

    else:
        if input[y][x] in ('/', '\\'):
            if xor(xd != 0, input[y][x] == '\\'):
                (xd, yd) = (yd, -xd)
            else:
                (xd, yd) = (-yd, xd)

        while True:
            x += xd
            y += yd

            if (not inside(x, y, input)):
                break
            
            if input[y][x] in ('/', '\\') or (input[y][x] in ('|', '-') and xor(xd != 0, input[y][x] == '-')):
                n.append((x,y,xd,yd))
                break

            r.append((x,y))

    return (r, n)

def findcoverage(v):
    global precalc

    visited = set()
    result = []

    unprocessed = [v]
    while len(unprocessed) > 0:
        v = unprocessed.pop()

        if v in visited:
            continue
        visited.add(v)

        if v in precalc:
            (r, n) = precalc[v]
        else:
            (r, n) = energize(v)
            precalc[v] = (r,n)

        unprocessed.extend(n)
        result.extend(r)

    return set(result)

r1 = len(findcoverage((0, 0, 1, 0)))

print("r1:", r1)

post.submit(r1, part="a", day=16)

r2 = 0

for v in faceinside(input):
    n = len(findcoverage(v))
    r2 = r2 if r2 > n else n

print("r2:", r2)

post.submit(r2, part="b", day=16)

