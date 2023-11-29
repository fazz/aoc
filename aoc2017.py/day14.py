
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re

input = data

def knothashround(input, memory, skip):
    size = 256
    pos = 0
    shift = 0
    for l in input:
        memory[pos:pos+l]=list(memory[pos:pos+l])[::-1]
        pos += (l + skip) % size
        skip += 1

        memory = memory[pos:size] + memory[0:pos]
        shift += pos
        pos = 0

    return (memory, shift, skip)

def knothash(input):

    shift = 0
    skip = 0
    size = 256
    memory = list(range(0, size))

    cinput2 = list(map(ord, input)) + [17, 31, 73, 47, 23]

    for c in range(64):
        (memory, extrashift, skip) = knothashround(cinput2, memory, skip)
        shift += extrashift

    memory = memory[(-shift)%size:] + memory[0:(-shift)%size]

    hash = [0]*16

    for i in range(16):
        hash[i] = reduce(operator.xor, memory[i*16:i*16+16], 0)
    
    return hash

field = defaultdict(int)

r1 = 0
for x in range(128):
    s = "{i}-{c}".format(i = input, c = x)
    h = knothash(s)
    for i in range(len(h)):
        v = h[i]
        z = 0
        while v > 0:
            if v & 1 == 1:
                r1 += 1
                field[128*x + i*8 + (7-z)] = 1
            z += 1
            v = v >> 1

post.submit(r1, part="a", day=14, year=2017)

visited = set()

r2 = 0

def bfs(x, y, visited):
    if (x,y) in visited:
        return (visited, 0)
    
    visited.add((x, y))

    for (xd, yd) in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        (x1, y1) = (x + xd,y + yd)
        if min(x1, y1) < 0 or max(x1, y1) > 127:
            continue
        if field[128*x1 + y1] == 1:
            (visited, _) = bfs(x1, y1, visited)

    return (visited, 1)

for k in tuple(field.keys()):
    x = k // 128
    y = k % 128

    (visited, count) = bfs(x, y, visited)
    r2 += count

post.submit(r2, part="b", day=14, year=2017)
