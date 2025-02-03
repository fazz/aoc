
from aocd import data, post
from collections import defaultdict
from aoc import inside

input = list(map(list, data.split('\n')))

roundedrocks = []

blocker = {v: {} for v in ((0, 1), (1, 0), (-1, 0), (0, -1))}

q = set()
for yi, y in enumerate(input):
    for xi, x in enumerate(y):
        if x != '#':
            for v in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                q.add((xi, yi, v))
            if x == 'O':
                roundedrocks.append((xi, yi))

def findblocker(xi, yi, v, q):
    xn = xi + v[0]
    yn = yi + v[1]
    q.discard((xn, yn, v))
    
    if (xn, yn) in blocker[v]:
        return blocker[v][(xn, yn)]
    
    if inside(xn, yn, input) and input[yn][xn] != '#':
        bp = findblocker(xn, yn, v, q)
        blocker[v][(xn, yn)] = bp
        return bp
    
    return (xn, yn)

while len(q) > 0:
    (xi, yi, v) = q.pop()
    blocker[v][(xi, yi)] = findblocker(xi, yi, v, q)

def singlemove(rr, v):
    b = blocker[v]
    be = defaultdict(lambda: 1)

    rrn = []
    while len(rr) > 0:
        (x, y) = rr.pop()
        bxy = b[(x,y)]
        bev = be[bxy]
        z = (bxy[0] - v[0]*bev, bxy[1] - v[1]*bev)

        be[bxy] += 1

        rrn.append(z)

    return rrn

def nw(pq):
    r = 0
    for (x, y) in pq:
        r += len(input) - y
    return r

r1 = 0

roundedrocks = singlemove(roundedrocks, (0, -1))

r1 = nw(roundedrocks)

print("r1:", r1)

post.submit(r1, part="a", day=14)

def h(rr):
    elements = sorted(rr)
    return tuple(elements)

history = {h(roundedrocks): 0}

def cycle(pq):
    pq = singlemove(pq, (0, -1))
    pq = singlemove(pq, (-1, 0))
    pq = singlemove(pq, (0, 1))
    pq = singlemove(pq, (1, 0))
    return pq

count = 1000000000

slack = None
csize = None
while True:
    rrn = cycle(roundedrocks)

    hc = h(rrn)
    if hc in history:
        slack = history[hc]
        csize = len(history) - slack
        break
    history[hc] = len(history)
    roundedrocks = rrn

p = ((count - slack) % csize) + slack

points = map(lambda f: f[0], filter(lambda e: e[1] == p, history.items()))
points = tuple(points)[0]
r2 = nw(points)

print("r2:", r2)

post.submit(r2, part="b", day=14)

