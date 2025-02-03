
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter, deque
from itertools import chain
from queue import PriorityQueue
from math import inf
from copy import copy
import operator
import re
import sys

from aoc import factor

input = data.split('\n')


if 0:
    input = [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#',    
    ]


if 0:
    input = [
    '#.#######',
    '#...#####',
    '#.#.#####',
    '#.....###',
    '###.#.###',
    '###...###',
    '#####.###',
    '#####...#',
    '#######.#',
    ]

dest = (len(input[0])-2, len(input)-1)

area = 0

for l in input:
    c = Counter(l).most_common(5)
    for cc in c:
        if cc[0] in ('.', '>', '^', '<', 'v'):
            area += cc[1]

print(area)



def nb(pos, v):

    (x, y) = pos

#    if input[y][x] == '<':
#        options = ((-1, 0),)
#    elif input[y][x] == '>':
#        options = ((1, 0),)
#    elif input[y][x] == 'v':
#        options = ((0, 1),)
#    elif input[y][x] == '^':
#        options = ((0, -1),)
#    else:
    options = ((0, 1), (1, 0), (-1, 0), (0, -1))

    for xd, yd in options:
        nx = x + xd
        ny = y + yd
        if (nx, ny) in v:
            continue
        if nx < 0 or ny < 0 or nx >= len(input[0]) or ny >= len(input):
            continue
        if input[ny][nx] not in ('.', '>', '^', '<', 'v'):
            continue
        yield (nx, ny)

#dest = (139, 140)

start = (1,0)

dist = defaultdict(lambda: -inf)

dist[start] = 0

visited = set()

stack = deque()
stack.append((start, set([start])))

def inways(pos, visited):

    nbs = [((n[0]-pos[0], n[1]-pos[1]), n) for n in nb(pos, visited)]

    r = len(nbs)

    #for (n, (nx, ny)) in nbs:
    #    if n == (0, 1) and input[ny][nx] == 'v':
    #        r -= 1
    #    elif n == (1, 0) and input[ny][nx] == '>':
    #        r -= 1
    #    elif n == (-1, 0) and input[ny][nx] == '<':
    #        r -= 1
    #    elif n == (0, -1) and input[ny][nx] == '^':
    #        r -= 1
    #if r == 1 and input[ny][nx] == '.':
    #    r = 0
    return r-1

#while len(stack) > 0:
#
#    (c, v) = stack.pop()
#    #print(c)
#    v = set(v)
#    #visited.add(c)
#
#    for n in nb(c, v):
#        if n == dest:
#            print(dist[n], dist[c])
#        if dist[n] < dist[c] + 1:
#            dist[n] = dist[c] + 1
#
#        #if inways(n, visited) == 0:
#        stack.appendleft((n, tuple(v.union([c]))))
#
#    #visited.remove(c)

r1 = dist[dest]

print("r1:", r1)

#post.submit(r1, part="a")


#post.submit(r2, part="b")

print("----------------------")

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

nodes = set()

for yi in range(len(input)):
    for xi in range(len(input[0])):
        if input[yi][xi] in ('.', '>', '^', '<', 'v'):
            nodes.add((xi, yi))


visited = set()
depth = defaultdict(int)
low = defaultdict(int)
parent = {}

def GetArticulationPoints(i, d):
    visited.add(i)
    depth[i] = d
    low[i] = d
    childCount = 0
    isArticulation = False

# 17,33

    for ni in nb(i, set()):
        if i == (15,31):
            print("ni", ni)

        if ni not in visited:
            parent[ni] = i
            for ap in GetArticulationPoints(ni, d + 1):
                yield ap
            childCount = childCount + 1
            if low[ni] >= depth[i]:
                isArticulation = True
            if i == (111111115, 32):
                print("isA:", isArticulation)
                print("ck:", childCount)
                print("p:", parent[i])
                print("d:", depth[i])
                print("l:", low[i], low[ni], ni)

                raise "z"
            low[i] = min(low[i], low[ni])
        elif ni != parent[i]:#???????
            if i == (15, 32):
                raise "z2"
            low[i] = min(low[i], depth[ni])
        if i == (15,31):
            print("LOW", ni, low[ni])

    if (i in parent and isArticulation) or (i not in parent and childCount > 1):
        if i == (15,32):
            raise "z"
        if len(tuple(nb(i, set()))) > 2 or len(tuple(nb(i, set()))) == 1:
            yield (i, parent[i])

    #visited.remove(i)


def dfscheck(node, target, visited):

    visited.add(node)

    for ni in nb(node, visited):
        if ni == target:
            return True
        r = dfscheck(ni, target, visited)
        if r:
            return True
    return False


#for n in nodes:
parent[start] = "ROOT"
for ap in GetArticulationPoints(start, 0):
    print(ap)

print("AP here")


#Start at a root node *root*
#Let D[i] = longest path from node *root* to node i. D[*root*] = 0, and the others are also 0.

longest = defaultdict(int)

visited = set()

def getLongestPath(node, target, currSum):
    if node in visited:
        return
    visited.add(node)

    if longest[node] < currSum:
        longest[node] = currSum
        if node == target:
            print(longest[target])

    if node != target:
        nbs = tuple(nb(node, visited))
        if len(nbs) > 1:
            nbs = filter(lambda x: dfscheck(x, target, copy(visited)), nbs)
        for n in nbs:
            getLongestPath(n, target, currSum + 1)

    visited.remove(node)

#start = (125, 123)
#visited.add((124, 123))
#visited.add((125, 122))
#target = dest
    
#start = (5, 11)
#target = (125, 123)
    
target = dest

getLongestPath(start, target, 0)

print(longest[target])


#r2 = 2460+155+27
# too low

# 6232+..?
# too low

#post.submit(r2, part="b")
# 6506!!!!!!!!!
    