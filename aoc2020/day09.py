import re

text_file = open("input09.txt", "r")

lines = [(lambda a: int(a))(x.rstrip("\n\r")) for x in text_file.readlines()]

step = 25
rolling = []
ints = []

part1 = 0

for x in lines:
    found = False

    if len(rolling) < step:
        found = True
    else:
        for i in range(len(rolling)-1):
            if x in rolling[i]:
                found = True
                break
        rolling.pop(0)
        ints.pop(0)

    rolling.append(set([x]))
    ints.append(x)
    for i in range(len(rolling)-1):
        rolling[i].add(ints[i]+x)

    if not found:
        part1 = x
        break

print("Part1:", part1)

ints = list(filter(lambda x: x < part1, lines))

lo = part1
hi = 0
found = False
for i in range(len(ints)):
    s = ints[i]
    for j in range(1,len(ints)-i):
        s += ints[i+j]
        if s > part1:
            break
        if s == part1:
            lo = min(ints[i:i+j+1])
            hi = max(ints[i:i+j+1])
            found = True
            break

    if found:
        break

print("Part2:", hi+lo)
