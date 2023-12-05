
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

r1 = 0

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

track = list(seeds)

for m in maps:
    nt = []
    for t in track:
        match = False
        for (dest, src, rl) in m:
            if src <= t and src+rl >= t:
                nt.append(t + (dest-src))
                match = True
        if not match:
            nt.append(t)

    track = nt            

r1 = min(track)

#################

r2 = 0

track = [(seeds[i*2], seeds[i*2+1]) for i in range(len(seeds)//2)]

for m in maps:

    nt = []

    for (tstart, tlen) in track:
        match = False

        srcranges = [(tstart, tlen)]

        for (dest, src, rl) in m:

            nranges = []
            for (tstart, tlen) in srcranges:

                firstbreak = None
                secondbreak = None

                if tstart < src and tstart + tlen >= src:
                    firstbreak = src - 1

                if tstart + tlen > src+rl and tstart < src+rl:
                    secondbreak = src + rl

                if firstbreak is not None and secondbreak is None:
                    nranges.append((tstart, firstbreak-tstart))
                    nt.append((firstbreak + (dest-src) + 1, tlen - (firstbreak-tstart)))

                if firstbreak is None and secondbreak is not None:
                    nranges.append((secondbreak, secondbreak-tstart+1))
                    nt.append((tstart + (dest-src), tlen - (secondbreak-tstart) - 1))

                if firstbreak is not None and secondbreak is not None:
                    nt.append((dest, rl))
                    nranges.append((tstart, firstbreak-tstart))
                    nranges.append((secondbreak, tstart+tlen-secondbreak))

                if firstbreak is None and secondbreak is None:
                    if tstart >= src and tstart + tlen <= src + rl:
                        nt.append((tstart + (dest-src), tlen))
                    else:
                        nranges.append((tstart, tlen))
            srcranges = nranges
        nt = nt + nranges
            
    track = nt

r2 = min([x[0] for x in track])

post.submit(r2, part="b")
