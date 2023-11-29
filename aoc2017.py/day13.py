
from aocd import data, post
import re

lines = data.split("\n")

layers = [tuple(map(int, re.split(': ', l))) for l in lines]

def penalty(delay, imm):
    caught = False
    ret = 0
    for l in layers:
        (d, w) = l

        if (delay + d) % ((w*2)-2) == 0:
            caught = True
            ret += (d * w)
        if imm and caught:
            break
    return (caught, ret)

post.submit(penalty(0, False)[1], part="a", day=13, year=2017)

d = 0
while True:
    if not penalty(d, True)[0]:
        break
    d += 1

post.submit(d, part="b", day=13, year=2017)
