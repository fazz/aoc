
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re

input = 324
#input = 3

buffer = [0]
p = 0

for i in range(1, 2018):
    p = (p + input) % len(buffer)
    if p+1 < len(buffer):
        r1 = buffer[p+1]
    buffer.insert(p+1, i)
    p = p+1

print(r1)

post.submit(r1, part="a", day=17, year=2017)

buffer = [0, -1]
blen = 1
p = 0

for i in range(1, 50000001):
    p = (p + input) % blen
    if p == 0:
        buffer[1] = i
        print(i, i % input )
    p = p+1
    blen += 1

r2 = buffer[1]
print(r2)

post.submit(r2, part="b", day=17, year=2017)

