
from aocd import data, post
from collections import defaultdict
from functools import cmp_to_key

input = data
#input = "2333133121414131402"

files = []
spaces = []

def getspace():
    for y in spaces:
        for x in range(y[0], y[1]+1):
            yield x

startcheck = 0

file = 0
pos = 0
for i, v in enumerate(input):
    sz = int(v)
    if i % 2 == 0:
        startcheck += sum([file*(pos+z) for z in range(sz)])

        files.append((file, pos, pos+sz-1))

        file += 1
    else:
        spaces.append([pos, pos+sz-1])

    pos += sz

spacegen = getspace()
nextspace = spacegen.__next__()

r1 = startcheck

for file in files[::-1]:
    for move in range(file[2], file[1]-1, -1):
        if move < nextspace:
            break
        r1 -= file[0]*move
        r1 += file[0]*nextspace

        nextspace = spacegen.__next__()

print(r1)

#r1 = calcl(input, 25)

post.submit(r1, part="a", day=9)

#r2 = calcl(input, 75)

#post.submit(r2, part="b", day=11)

r2 = startcheck

for file in files[::-1]:
    fsz = file[2] - file[1] + 1

    for si, space in enumerate(spaces):
        ssz = space[1] - space[0] + 1
        if space[0] > file[1]:
            break
        if fsz <= ssz:

            r2 -= sum([file[0]*z for z in range(file[1], file[2]+1)])
            r2 += sum([file[0]*z for z in range(space[0], space[0]+fsz)])

            if fsz < ssz:
                spaces[si] = [space[0]+fsz, space[1]]
            else:
                spaces.pop(si)
            break

print(r2)

post.submit(r2, part="b", day=9)
