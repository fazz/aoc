
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

s = input[0][7:]

seeds = tuple(map(int, s.split()))

maps = []
cm = []

for li in range(2, len(input)+1):
    if li >= len(input) or len(input[li]) == 0:
        maps.append(cm)
        cm = []
    elif not input[li][0].isdigit():
        pass
    else:
        l = tuple(map(int, input[li].split()))
        cm.append(l)

wseeds = [(seeds[i*2], seeds[i*2+1]) for i in range(len(seeds)//2)]

def calc(wseeds):

    for m in maps:

        nt = []

        for (tstart, tlen) in wseeds:
            srcranges = [(tstart, tlen)]

            for (dest, src, rl) in m:

                nranges = []
                for (tstart, tlen) in srcranges:

                    left = (    
                        tstart,
                        max(min(src - tstart, tlen), 0)
                    )

                    right = (
                        max(tstart, src + rl),
                        max(min(tlen - ((src + rl) - tstart), tlen), 0)
                    )

                    middle = (
                        max(src, tstart),
                        max(min(src + rl, tstart + tlen) - max(src, tstart), 0)
                    )

                    if middle[1] > 0:
                        middle = (middle[0] + (dest-src), middle[1])
                        nt.append(middle)

                    if left[1] > 0:
                        nranges.append(left)
                    if right[1] > 0:
                        nranges.append(right)

                srcranges = nranges
            nt = nt + nranges
        wseeds = nt
    return min([x[0] for x in wseeds])

wseeds = [(x, 1) for x in seeds]

r1 = calc(wseeds)

post.submit(r1, part="a")

wseeds = [(seeds[i*2], seeds[i*2+1]) for i in range(len(seeds)//2)]

r2 = calc(wseeds)

post.submit(r2, part="b")
