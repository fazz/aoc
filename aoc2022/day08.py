
from functools import reduce
import operator
from collections import defaultdict

trees = [list(map(int, x.rstrip("\n\r"))) for x in open("input08.txt", "r").readlines()]

linelen = len(trees[0])
height = len(trees)

def out(i, j):
    return i < 0 or j < 0 or i >= height or j >= linelen

def edge(i, j):
    return i == 0 or j == 0 or (i == height-1) or (j == linelen-1)

def calc(i, j):
    vector = (0, 1)
    dist = 1
    scores = defaultdict(int)
    visible = False
    blocked = set()

    while len(blocked) < 4:
        for _ in range(4):
            vector = (-vector[1], vector[0])
            if vector not in blocked:
                (x, y) = (i+vector[0]*dist, j+vector[1]*dist)

                if out(x, y):
                    visible = True
                    blocked.add(vector)
                else:
                    scores[vector] += 1
                    b = trees[x][y] >= trees[i][j] 
                    if b or edge(x, y):
                        blocked.add(vector)
                        visible = True if not b else visible
        dist += 1

    return (visible, reduce(operator.mul, scores.values(), 1))

r = [calc(i,j) for i in range(height) for j in range(linelen)]

print("Part1:", len([x for x in r if x[0]]))
print("Part2:", max([x[1] for x in r]))
