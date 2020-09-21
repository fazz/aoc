
from math import gcd

text_file = open("input10.txt", "r")
lines = [l.strip() for l in text_file.readlines()]

asteroids = set()

for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == '#':
            asteroids.add((x,y))

visibility = {}

def tobase(x, y):
    g = gcd(x,y)
    return (x // g, y // g)

for a in asteroids:
    diffset = set([tobase(o[0] - a[0], o[1] - a[1]) for o in asteroids.difference({a})])
    visibility.setdefault(a, diffset)
    s = visibility[a]

m = max([len(a) for a in visibility.values()])
print(m)

# 2nd part input
print([a[0] for a in visibility.items() if len(a[1]) == m])

