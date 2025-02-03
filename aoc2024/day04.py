
import sys
sys.path.insert(0, "../aoc2023")

from aocd import data, post
from aoc import inside, vector8segments, vector4diagonal

input = data.split('\n')

def detect(p, v, tocheck):
    if len(tocheck) == 0:
        return 1
    (x,y) = (p[0] + v[0], p[1] + v[1])
    if inside(x, y, input) and input[y][x] == tocheck[0]:
        return detect((x,y), v, tocheck[1:])
    else:
        return 0

r1 = 0
r2 = 0
for y in range(len(input)):
    for x in range(len(input[0])):
        if input[y][x] == 'X':
            for v in vector8segments():
                r1 += detect((x,y), v, list('MAS'))

        if input[y][x] == 'A':
            c = 0
            for v in list(vector4diagonal())[:2]:
                for (a,b) in (('S', 'M'), ('M', 'S')):
                    if inside(x+v[0], y+v[1], input) and input[y+v[1]][x+v[0]] == a:
                        if inside(x-v[0], y-v[1], input) and input[y-v[1]][x-v[0]] == b:
                            c += 1
                            break
            if c == 2:
                r2 += 1

post.submit(r1, part="a", day=4)
post.submit(r2, part="b", day=4)
