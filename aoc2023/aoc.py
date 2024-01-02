
from collections import Counter, defaultdict
from functools import reduce
from itertools import chain
import operator

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

