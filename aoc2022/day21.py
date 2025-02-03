import datetime
from copy import deepcopy, copy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

lines = [x.rstrip(" \n\r") for x in open("input21.txt", "r")]

entries = {}

ops = { '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv }

for l in lines:
    i = l.index(':')
    src = l[0:i]
    dst = l[i+2:].split(' ')
    if len(dst) == 1:
        entry = [int(dst[0])]
    else:
        (opr1, op, opr2) = dst
        entry = [ops[op], opr1, opr2, None, None]

    entries[src] = entry

for (e,v) in entries.items():
    if len(v) == 1:
        continue
    (r1, r2) = (entries[v[1]], entries[v[2]])
    v[3] = r1
    v[4] = r2

def fold(name, v, target):
    if name == target:
        return target

    if len(v) == 1:
        return v[0]

    r1 = fold(v[1], v[3], target)
    r2 = fold(v[2], v[4], target)

    if isinstance(r1, int) and isinstance(r2, int):
        return v[0](r1, r2)

    return [v[0], r1, r2]

print("Part 1:", fold("root", entries["root"], None))

f1 = fold(entries["root"][1], entries[entries["root"][1]], "humn")
f2 = fold(entries["root"][2], entries[entries["root"][2]], "humn")

if isinstance(f1, int):
    (wanted, model) = (f1, f2)
else:
    (wanted, model) = (f2, f1)

rop1 = {
    operator.mul: operator.floordiv,
    operator.floordiv: lambda x, y: y // x,
    operator.add: operator.sub,
    operator.sub: lambda x, y: y - x
}

rop2 = {
    operator.mul: operator.floordiv,
    operator.floordiv: operator.mul,
    operator.add: operator.sub,
    operator.sub: operator.add
}

def turn(wanted, model):
    if model == 'humn':
        return wanted

    if isinstance(model[1], int):
        o = rop1[model[0]]
        return turn(o(wanted, model[1]), model[2])
    else:
        o = rop2[model[0]]
        return turn(o(wanted, model[2]), model[1])

print("Part 2:", turn(wanted, model))
