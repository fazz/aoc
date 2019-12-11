
from math import gcd, atan2, pi
from functools import cmp_to_key

text_file = open("input10.txt", "r")
lines = [l.strip() for l in text_file.readlines()]

stationx = 29
stationy = 28

asteroids = set()

for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == '#' and (x, y) != (stationx, stationy):
            asteroids.add((stationy-y, x-stationx))

bases = {}

for a in asteroids:
    g = gcd(a[0], a[1])
    bases.setdefault((a[0] // g, a[1] // g), set()).add(a)

def atan2full(y, x):
    v = atan2(y, x)
    return 2*pi + v if v < 0 else v

sortedbases = sorted(bases.keys(), key = cmp_to_key( lambda i1, i2: atan2full(i1[1], i1[0]) - atan2full(i2[1], i2[0])))

itemno = 1
lastblown = (0,0)
currentbaseidx = -1

while itemno <= 200:
    while True:
        currentbaseidx = (currentbaseidx + 1) % len(sortedbases)
        base = sortedbases[currentbaseidx]
        if len(bases[base]) > 0:
            lastblown = min(bases[base])
            bases[base].remove(lastblown)
            itemno += 1
            break

realx = lastblown[1]+stationx
realy = stationy-lastblown[0]

print(100*realx+realy)
