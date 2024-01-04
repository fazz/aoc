
from aocd import data, post

input = data.split('\n')

doubler = set()
doublec = set()

galaxies = set()

for yi in range(len(input)):
    if not '#' in input[yi]:
        doubler.add(yi)
    else:
        galaxies = galaxies.union([(i, yi) for i, c in enumerate(input[yi]) if c == '#'])

for xi in range(len(input[0])):
    check = True
    for yi in range(len(input)):
        if (xi, yi) in galaxies:
            check = False
            break
    if check:
        doublec.add(xi)

galaxies = tuple(galaxies)

def calc(rate):

    r = 0

    for gi in range(len(galaxies)):
        g = galaxies[gi]
        for g2i in range(gi+1, len(galaxies)):
            g2 = galaxies[g2i]
            r += abs(g2[0]-g[0]) + abs(g2[1]-g[1])

            r += (rate-1) * len(doublec.intersection(range(min(g[0], g2[0])+1, max(g[0], g2[0]))))

            r += (rate-1) * len(doubler.intersection(range(min(g[1], g2[1])+1, max(g[1], g2[1]))))

    return r

r1 = calc(2)

post.submit(r1, part="a", day=11)

r2 = calc(1000000)

post.submit(r2, part="b", day=11)
