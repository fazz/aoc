
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter, deque
from itertools import chain
import operator
import re
import sys
from queue import PriorityQueue


from aoc import factor

input = data.split('\n')

xinput = [
    
'1,0,1~1,2,1',
'0,0,2~2,0,2',
'0,2,3~2,2,3',
'0,0,4~0,2,4',
'2,0,5~2,2,5',
'0,1,6~2,1,6',
'1,1,8~1,1,9',
]

#r1 = calc(2)

bricks = list()

for l in input:
    (l, r) = l.split('~')

    lc = tuple(map(int, l.split(',')))
    rc = tuple(map(int, r.split(',')))

    bricks.append((lc, rc))


zcoord = {}

# klotsi ülemine pind
def findz(brick, lower=False):

    vlen = abs(brick[0][2] - brick[1][2]) + 1

    if brick in zcoord:
        if lower:
            return zcoord[brick] - vlen + 1
        return zcoord[brick]
    
    minz = min(brick[0][2], brick[1][2])
    maxz = max(brick[0][2], brick[1][2])

    if minz == 1:
        zcoord[brick] = maxz
        if lower:
            return 1
        return zcoord[brick]

    zs = [0]

    for b2 in bricks:
        if b2 == brick:
            continue
        minz2 = min(b2[0][2], b2[1][2])
        if minz2 >= maxz:
            continue
        if overlap(brick, b2):
            zs.append(findz(b2))
    r = max(zs) + vlen
    zcoord[brick] = r
    if lower:
        return r - vlen + 1
    return r


overlapcache = {}
def overlap(b, b2):
    global overlapcache

    if (b, b2) in overlapcache:
        return overlapcache[(b, b2)]

    coord = set()
    coord2 = set()

    for x in range(min(b[0][0], b[1][0]), max(b[0][0], b[1][0])+1):
        for y in range(min(b[0][1], b[1][1]), max(b[0][1], b[1][1])+1):
            coord.add((x, y))

    for x in range(min(b2[0][0], b2[1][0]), max(b2[0][0], b2[1][0])+1):
        for y in range(min(b2[0][1], b2[1][1]), max(b2[0][1], b2[1][1])+1):
            coord2.add((x, y))
            
    v = len(coord2.intersection(coord)) > 0

    overlapcache[(b, b2)] = v
    overlapcache[(b2, b)] = v

    return v

underlings = {}
def supportcount(brick, removed=set()):
    global underlings

    if brick in underlings:
        return len(underlings[brick].difference(removed))
    
    underlings[brick] = set()

    for b in bricks:
        if supportedby(b, brick):
            underlings[brick].add(b)

    return len(underlings[brick].difference(removed))

support = {}
def supportedby(lower, upper=None):
    global support

    if lower in support:
        if upper is not None:
            return upper in support[lower]
        return support[lower]

    support[lower] = set()

    for b in bricks:
        if b == lower:
            continue
        if overlap(b, lower) and findz(lower) == findz(b, lower=True)-1:
            support[lower].add(b)

    if upper is not None:
        return upper in support[lower]
    return support[lower]


removable = 0

for b in bricks:
    flag = True
    for b2 in supportedby(b):
        sc = supportcount(b2)

        if sc < 2:
            flag = False
            break

    if flag:
        removable += 1

r1 = removable

print("r1:", r1)

post.submit(r1, part="a")

upperscache = {}

def supported(obrick):

    q = PriorityQueue()

    removed = set()

    q.put((findz(obrick), obrick))
    removed.add(obrick)

    while not q.empty():

        (z, brick) = q.get()
        #z = findz(brick)

        #c = set()
        #for e in removed:
        #    if findz(e) >= z:
        #        c.add(e)
        c = removed

        #
        # Võtad klotsi, arvestades seda, mis on eemaldatud hetkeks, kui selle klotsi võtad.
        # Õigemini, klots on osa mingist juba eemaldatud komplektist.
        # Cachemine: kui konkreetsel tasemel või sellest kõrgemal on eemaldatud klotside hulk X, siis edasi eemaldatakse veel klotside hulk Y
        #
        #
        #

        if (brick, tuple(c)) in upperscache:
            uppers = upperscache[(brick, tuple(c))]
        else:
            uppers = set()

            for b in supportedby(brick):
                if supportcount(b, removed) < 1:
                    uppers.add(b)
                    q.put((findz(b), b))

            upperscache[(brick, tuple(c))] = uppers

        removed.add(brick)
        removed = removed.union(uppers)

    return removed

r2 = 0

for b in bricks:
    v = len(supported(b))-1
    #print("v:", v)
    r2 += v


print("r2:", r2)

#print(upperscache)


#r2 = calc(1000000)

post.submit(r2, part="b")
#108487 too high


#1,0,1~1,2,1   <- A
#0,0,2~2,0,2   <- B
#0,2,3~2,2,3   <- C
#0,0,4~0,2,4   <- D
#2,0,5~2,2,5   <- E
#0,1,6~2,1,6   <- F
#1,1,8~1,1,9   <- G