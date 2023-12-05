
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

r1 = 0

symbols = set()

for yi in range(len(input)):
    for xi in range(len(input[0])):
        if not (input[yi][xi].isdigit() or input[yi][xi] == '.'):
            symbols.add((xi, yi))

state = 0

gearcandidates = defaultdict(list)

state = 0
number = 0
coords = []
gears = set()

for yi in range(len(input)):
    for xi in range(len(input[0])+1):
        if xi < len(input[0]) and input[yi][xi].isdigit():
            if state == 0:
                state = 1
                number = 0
                coords = []
            number = number * 10 + int(input[yi][xi])
            coords.append((xi, yi))
        elif state == 1:
            state = 0

            check = False
            for yy in range(coords[0][1]-1, coords[0][1] + 2):
                for xx in range(coords[0][0]-1, coords[-1][0] + 2):
                    if (xx, yy) in symbols:
                        check = True
                        if input[yy][xx] == '*':
                            gears.add((xx, yy))
            if check:
                r1 += number
 
                for (xx, yy) in gears:
                    gearcandidates[(xx, yy)].append(number)

            number = 0
            coords = []
            gears = set()

post.submit(r1, part="a")

r2 = sum(map(lambda y: y[1][0]*y[1][1], filter(lambda x: len(x[1]) == 2, gearcandidates.items())))

post.submit(r2, part="b")

