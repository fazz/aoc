
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

def calc(input):
    r = 0
    for l in input:
        d = list(filter(lambda x: x.isdigit(), l))
        r += 10*int(d[0]) + int(d[-1])
    return r

r1 = calc(input)

post.submit(r1, part="a")

def rep(l):
    l = l.replace('one', 'o1e')
    l = l.replace('two', 't2')
    l = l.replace('three', 't3e')
    l = l.replace('four', '4')
    l = l.replace('five', '5e')
    l = l.replace('six', '6')
    l = l.replace('seven', '7n')
    l = l.replace('eight', '8t')
    l = l.replace('nine', '9e')

    return l

r2 = calc(map(rep, input))

post.submit(r2, part="b")
