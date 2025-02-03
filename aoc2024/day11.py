
from aocd import data, post
from collections import defaultdict
from functools import cmp_to_key

input = list(map(int, data.split(' ')))

cache = {}

def calcl(stones, it):
    return sum([calc(s, it) for s in stones])

def calc(stone, it):
    if it == 0:
        return 1
    if (stone, it) in cache:
        return cache[(stone, it)]
    
    sn = []
    if stone == 0:
        sn.append(1)
    elif len(str(stone)) % 2 == 0:
        x = len(str(stone)) // 2
        sn.append(stone // 10**x)
        sn.append(stone % (10**x))
    else:
        sn.append(stone * 2024)

    ret = calcl(sn, it-1)

    cache[(stone, it)] = ret
    return ret
    

r1 = calcl(input, 25)

post.submit(r1, part="a", day=11)

r2 = calcl(input, 75)

post.submit(r2, part="b", day=11)
