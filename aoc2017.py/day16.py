
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re

input = data
amt = 16

moves = input.split(',')

p = list(range(amt))

def dance(p):
    for m in moves:
        if m[0] == 's':
            a = int(m[1:])
            p = p[amt-a:] + p[0:amt-a]
        else:
            if m[0] == 'x':
                (a, b) = map(int, m[1:].split('/'))
            else:
                (a, b) = map(lambda x: p.index(ord(x) - ord('a')), m[1:].split('/'))
            t = p[b]
            p[b] = p[a]
            p[a] = t
    return p

p = dance(p)

r1 = ''.join([chr(x + ord('a')) for x in p])
post.submit(r1, part="a", day=16, year=2017)

for i in range(1000000000%30-1):
    p = dance(p)

r2 = ''.join([chr(x + ord('a')) for x in p])

post.submit(r2, part="b", day=16, year=2017)
