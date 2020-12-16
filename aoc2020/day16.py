
from functools import reduce
from itertools import product

text_file = open("input16.txt", "r")
lines = [x.rstrip("\n\r") for x in text_file.readlines()]

part1 = 0

sets = {}
allvalues = set()
validtickets = []
yourticket = []
phase = 0
for l in lines:
    if len(l) == 0:
        continue
    if l[0:4] == 'your':
        phase = 1
        continue
    if l[0:6] == 'nearby':
        phase = 2
        continue
    if phase == 0:
        (name, other) = l.split(':')
        ranges = other.lstrip().split(' or ')
        for r in ranges:
            r2 = set(range(*map(int, r.split('-'))))
            r2.add(max(r2)+1)
            sets.setdefault(name, set()).update(r2)
            allvalues.update(r2)
    elif phase == 1:
        yourticket = list(map(int, l.split(',')))
    elif phase == 2:
        values = [(v, False) for v in map(int, l.split(','))]
        (er, error) = reduce(lambda x,y: (x[0] + (y[0] if y[0] not in allvalues else 0), x[1] or (y[0] not in allvalues)), values, (0, False))
        part1 += er
        if not error:
            validtickets.append([x[0] for x in values])

print("Part1:", part1)

rl = len(validtickets[0])
names = {n: set(range(rl)) for n in sets.keys()}

singles = set()
for (i, val) in map(lambda x: (x[0], x[1][x[0]]), product(range(rl),validtickets)):
    for name in sets.keys():
        if val not in sets[name] and i in names[name]:
            names[name].remove(i)
            if len(names[name]) == 1:
                singles.update(names[name])

while len(singles) < rl:
    for p in filter(lambda x: len(names[x]) > 1, names.keys()):
        names[p] = names[p].difference(singles)
        if len(names[p]) == 1:
            singles.update(names[p])

dep = [list(x[1])[0] for x in filter(lambda x: x[0][0:3] == 'dep', names.items())]
part2 = reduce(lambda x,y: x*y,[yourticket[d] for d in dep] , 1)

print("Part2:", part2)
