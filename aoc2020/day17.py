from functools import reduce
from itertools import product
from copy import deepcopy

text_file = open("input17.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

space = {}

lx = 0
ux = 0
ly = 0
uy = 0
lz = 0
uz = 0

activated = 0

for y in range(len(lines)):
    if y > uy:
        uy = y
    for x in range(len(lines[y])):
        if x > ux:
            ux = x
        on = lines[y][x] == '#'
        space.setdefault(x, {}).setdefault(y, {})[0] = on
        if on:
            activated += 1


def get(x,y,z,space):
    return space.setdefault(x, {}).setdefault(y, {}).setdefault(z, False)

def newstate(x,y,z,space):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == dy == dz == 0:
                    continue
                count += 1 if get(x+dx,y+dy,z+dz,space) else 0
    a = get(x,y,z,space)
    if a and count in [2,3]:
        return (True, False)
    if not a and count in [3]:
        return (True, True)
    return (False, a) # TODO kas qige?

for round in range(6):

    newspace = deepcopy(space)

    for x in range(lx - 1, ux + 2):
        for y in range(ly - 1, uy + 2):
            for z in range(lz - 1, uz + 2):
                (state, changed) = newstate(x,y,z,space)
                newspace.setdefault(x, {}).setdefault(y, {})[z] = state
                if changed:
                    if state:
                        activated += 1
                    else:
                        activated -= 1

    lx -= 1
    ux += 1
    ly -= 1
    uy += 1
    lz -= 1
    uz += 1
    space = newspace

print("Part1", activated, 368)

#
#
#

# x -> y -> z
rounds = 6
dm = 4
space = {x: {y: {z: {} if dm > 3 else False for z in range(-rounds-1, rounds+1)} for y in range(-rounds-1, len(lines)+rounds+1)} for x in range(-rounds-1, len(lines[0])+rounds+1)}

dimensions = [set({-1,0,1}) for x in range(dm)]

activated = 0

def setpos(ds, space, value):
    for d in ds[0:-1]:
        space = space[d]
    space[ds[-1]] = value

for y in range(len(lines)):
    dimensions[1].add(y+1)
    activated += lines[y].count('#')
    for x in range(len(lines[y])):
        dimensions[0].add(x+1)
        on = lines[y][x] == '#'
        setpos([x,y,0,0], space, on)

def get2(x,y,z,w,space):
    return space[x][y].setdefault(z, {}).setdefault(w, False)

def newstate2(coord,space):
    count = 0
    (x,y,z,w) = coord
    zeroes = tuple([0] * len(coord))
    for (dx, dy, dz, dw) in product([-1, 0, 1], repeat = len(coord)):
        if (dx, dy, dz, dw) == zeroes:
            continue
        count += 1 if get2(x+dx,y+dy,z+dz,w+dw,space) else 0

    a = get2(x,y,z,w,space)
    if a and count in [2,3]:
        return (True, False)
    if not a and count in [3]:
        return (True, True)
    return (False, a) # TODO kas qige?

for round in range(6):

    newspace = deepcopy(space)

    for coord in product(*dimensions):
        (state, changed) = newstate2(coord,space)
        setpos(coord, newspace, state)
        activated += 0 if not changed else (1 if state else -1)

    for d in dimensions:
        d.add(min(d)-1)
        d.add(max(d)+1)

    space = newspace

print("Part2", activated, 2696)
