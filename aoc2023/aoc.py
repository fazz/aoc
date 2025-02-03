
from collections import Counter, defaultdict, deque
from functools import reduce
from itertools import chain
from heapq import *
import operator
import math

generated_primes = [2]

def primes(last):
    c = set(range(generated_primes[-1]+1, last+1))
    for p in generated_primes:
        yield p
        c = set(filter(lambda x: x%p != 0, c))
    while len(c) > 0:
        p = min(c)
        yield p
        generated_primes.append(p)
        c.remove(p)
        c = set(filter(lambda x: x%p != 0, c))

def factor(x):
    for p in primes(x):
        while x % p == 0:
            yield p
            x = x // p
            if x == 1:
                return

def lcm_c(d, t):
    d[t[0]] = max(d[t[0]], t[1])
    return d

def lcm(numbers):
    z = [xx for x in map(lambda x: Counter(factor(x)).items(), numbers) for xx in x]
    z = reduce(lcm_c, z, defaultdict(int))
    return reduce(lambda o, t: o*(t[0]**t[1]), z.items(), 1)

def vector8segments():
    d = (1,0)
    for _ in range(4):
        yield d
        yield (d[0] - d[1], d[0] + d[1])
        d = (-d[1], d[0])

def vector4diagonal():
    d = (1,1)
    for _ in range(4):
        yield d
        d = (-d[1], d[0])

#####

def all_pairwise_undirected(elements):
    for i in range(len(elements)):
        for j in range(i+1, len(elements)):
            yield (elements[i], elements[j])


#####
            
def raycross2D(s1, s2):
    ((px1, py1), (sx1, sy1)) = s1
    ((px2, py2), (sx2, sy2)) = s2

    dx = px2 - px1
    dy = py2 - py1
    det = sx2 * sy1 - sy2 * sx1
    if det != 0:
        u = (dy * sx2 - dx * sy2) / det
        v = (dy * sx1 - dx * sy1) / det

        ex = px1 + u * sx1
        ey = py1 + u * sy1

        if u > 0 and v > 0:
            return (ex, ey)
    return None

            
def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def norm2(v):
    return v[0]**2 + v[1]**2 + v[2]**2

def norm(v):
    return sqrt(norm2(v))

def cross(b, c):
    return (b[1] * c[2] - c[1] * b[2], b[2] * c[0] - c[2] * b[0], b[0] * c[1] - c[0] * b[1])

def intersection(a, b):
# http://mathworld.wolfram.com/Line-LineIntersection.html
# in 3d; will also work in 2d if z components are 0
    
    ((ax, ay, az), av) = a
    ((bx, by, bz), bv) = b
    
    da = av
    db = bv
    dc = (bx-ax, by-ay, bz-az)

    if (dot(dc, cross(da,db)) != 0.0): # lines are not coplanar
        return (False, None, True)

    s = dot(cross(dc,db),cross(da,db)) / norm2(cross(da,db))
    t = dot(cross(dc,da),cross(da,db)) / norm2(cross(da,db))

    if True: #(s >= 0.0 and s <= 1.0):
        ip = (s * da[0] + ax,s * da[1] + ay,s * da[2] + az)

        if tuple(map(int, ip)) == ip:
            return (True, ip, False)
    return (False, None, False)


#####

def hammingdistance(a, b):
    r = 0
    for i, c in enumerate(a):
        if c != b[i]:
            r += 1
    return r

def transposestringmatrix(m):
    r = ["" for x in range(len(m[0]))]
    for row in m:
        for i, c in enumerate(row):
            r[i] += c
    return r


######

def filtersplit(func, it):

    tb = deque()
    fb = deque()

    it = it.__iter__()

    tit = _filtersplit(func, tb, fb, it)
    fit = _filtersplit(lambda x: not func(x), fb, tb, it)

    return (tit, fit)
    
class _filtersplit:
    def __init__(self, func, buffer, otherbuffer, iterable):
        self.func = func
        self.buffer = buffer
        self.otherbuffer = otherbuffer
        self.iterable = iterable

    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.buffer) > 0:
            return self.buffer.popleft()
        while True:
            v = next(self.iterable)
            if self.func(v):
                return v
            else:
                self.otherbuffer.append(v)



######

def inside(x, y, matrix):
    return y >= 0 and x >= 0 and y < len(matrix) and x < len(matrix[0])

def inside2(x, y, maxx, maxy):
    return y >= 0 and x >= 0 and y <= maxy and x <= maxx

# TODO add offset
def faceinside(matrix):
    my = len(matrix)
    mx = len(matrix[0])

    for z in range(mx):
        yield (z, 0, 0, 1)
        yield (z, my-1, 0, -1)

    for z in range(my):
        yield (0, z, 1, 0)
        yield (mx-1, z, -1, 0)


######

def uniform_cost_search(start, neighbors):
    frontier = []
    heappush(frontier, (0, start))
    frontiertrack = {start:0}

    expanded = {}

    while True:
        if len(frontier) == 0:
            break
        (cost, node) = heappop(frontier)
        if node not in frontiertrack:
            continue
        del frontiertrack[node]
        # No goal checking implemented
        expanded[node] = cost
        for (nbc, nb) in neighbors(node):
            ncost = cost + nbc
            if nb not in expanded and nb not in frontiertrack:
                heappush(frontier, (ncost, nb))
                frontiertrack[nb] = ncost
            elif nb in frontiertrack and frontiertrack[nb] > ncost:
                heappush(frontier, (ncost, nb))
                frontiertrack[nb] = ncost

    return expanded

#####

def astar_path(camefrom, current):
    total_path = []
    (cs, current) = current
    while True:
        total_path = [(cs, current)] + total_path
        if current not in camefrom.keys():
            break
        (cs, current) = camefrom[current]
    return total_path

def astar(start, verifygoal, neighbors, h, compute_path=False):

    openset = []

    heappush(openset, (0, start))

    camefrom = {}

    gscore = defaultdict(lambda: math.inf)
    gscore[start] = 0

    i = 0
    while len(openset) > 0:
        c = heappop(openset)
        (cfscore, cnode) = c
        if verifygoal(cnode):
            return (cfscore, astar_path(camefrom, c))
        
        cgscore = gscore[cnode]
        for (dnext, next) in neighbors(cnode):
            tentative_gScore = cgscore + dnext
            if tentative_gScore < gscore[next]:
                if compute_path:
                    camefrom[next] = (cgscore, cnode)
                gscore[next] = tentative_gScore
                heappush(openset, (tentative_gScore + h(next), next))

    raise "Failure to compute A*"

