import re
from itertools import chain
from functools import reduce
from copy import deepcopy

text_file = open("input21.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

altofood = {}
foodcount = {}
singles = set()

for l in lines:

    (front, back) = l.split('(')

    for food in front.strip().split(' '):
        foodcount.setdefault(food, 0)
        foodcount[food] += 1

    for al in back[9:-1].split(', '):
        s = set([food for food in front.strip().split(' ')])
        altofood.setdefault(al, s)
        altofood[al] = altofood[al].intersection(s)
        if len(altofood[al]) == 1:
            singles = singles.union(altofood[al])

present = set(chain(*altofood.values()))
part1 = sum([(lambda x: x[1] if x[0] not in present else 0)(x) for x in foodcount.items()])

print("Part1:", part1)

while len(singles) > 0:
    r = singles.pop()
    for (k, v) in altofood.items():
        if len(v) > 1:
            if r in v:
                v.remove(r)
            if len(v) == 1:
                singles = singles.union(v)

print("Part2:", ','.join([list(x[1])[0] for x in sorted(altofood.items(), key=lambda x: x[0])]))
