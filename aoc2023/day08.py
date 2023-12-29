
from aocd import data, post
from functools import reduce
from itertools import chain
import operator

from aoc import lcm

input = data.split('\n')

instructions = input[0]

d = { 'R': 1, 'L': 0 }

moves = {}

for e in input[2:]:
    s = e[0:3]

    l = e[7:10]
    r = e[12:15]

    moves[s] = (l, r)

def calc(startfilter):

    currents = list(filter(startfilter, moves.keys()))
    cycles = {}

    ci = 0
    step = 0

    while True:
        for statei in range(len(currents)):
            if statei in cycles:
                continue
            currents[statei] = moves[currents[statei]][d[instructions[ci]]]

            if currents[statei][2] == 'Z':
                cycles[statei] = step + 1

        if len(cycles) == len(currents):
            break
        step += 1
        ci = (ci + 1) % len(instructions)

    return lcm(cycles.values())

r1 = calc(lambda x: x == 'AAA')

post.submit(r1, part="a", day=8)

r2 = calc(lambda x: x[2] == 'A')

post.submit(r2, part="b", day=8)

