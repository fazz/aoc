
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

startfield = [
    '.#.',
    '..#',
    '###'
]

# tuple-in-tuple to translation
transl = {}

def rotate90CClockwise(size, matrix):

    new = tuple(list() for x in range(size))

    for i in range(size):
        for j in range(size):
            new[size - j - 1].append(matrix[i][j])

    return tuple(map(lambda x: ''.join(x), new))

def parse(line):
    (a, b) = line.split(' => ')
    src = tuple(a.split('/'))
    target = tuple(b.split('/'))
    return (src, target)

for line in input:
    (src, target) = parse(line)

    for i in range(2):
        for j in range(4-i):
            src = rotate90CClockwise(len(src), src)
            if src not in transl:
                transl[src] = target

        src = tuple(map(lambda x: x[::-1], src))

def calc(count):
    field = startfield
    for x in range(count):
        size = len(field)
        stage = 2 if size % 2 == 0 else 3
        nsize = (size//2)*3 if stage == 2 else (size//3)*4
        mult = 3 if stage == 2 else 4

        nfield = [list() for _ in range(nsize)]

        for yc in range(size // stage):
            subf = field[yc*stage:(yc+1)*stage]
            for xc in range(size // stage):
                t = transl[tuple(z[xc*stage:(xc+1)*stage] for z in subf)]
                for z in range(mult):
                    nfield[(yc*mult)+z].append(t[z])

        field = list(map(lambda x: ''.join(x), nfield))
    return ''.join(field).count('#')

r1 = calc(5)
post.submit(r1, part="a", day=21, year=2017)

r2 = calc(18)
post.submit(r2, part="b", day=21, year=2017)
