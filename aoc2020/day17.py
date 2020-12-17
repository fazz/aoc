from functools import reduce
from itertools import product
from copy import deepcopy

text_file = open("input17.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]


# x -> y -> z
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
    print("count:", count)
    a = get(x,y,z,space)
    if a and count in [2,3]:
        return (True, False)
    if not a and count in [3]:
        return (True, True)
    return (False, a) # TODO kas qige?


def prints(space):

    for z in sorted(space[0][0].keys()):
        print("z:", z)
        for y in sorted(space[0].keys()):
            for x in sorted(space.keys()):
                print('#' if space[x][y][z] else '.', end="")
            print()

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

    #prints(newspace)
    lx -= 1
    ux += 1
    ly -= 1
    uy += 1
    lz -= 1
    uz += 1
    space = newspace

print("Part1", activated)

#
#
#

# x -> y -> z
space = {}

lx = 0
ux = 0
ly = 0
uy = 0
lz = 0
uz = 0
lw = 0
uw = 0

activated = 0

for y in range(len(lines)):
    if y > uy:
        uy = y
    for x in range(len(lines[y])):
        if x > ux:
            ux = x
        on = lines[y][x] == '#'
        space.setdefault(x, {}).setdefault(y, {}).setdefault(0, {})[0] = on
        if on:
            activated += 1


def get2(x,y,z,w,space):
    return space.setdefault(x, {}).setdefault(y, {}).setdefault(z, {}).setdefault(w, False)

def newstate2(x,y,z,w,space):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dw in [-1, 0, 1]:
                    if dx == dy == dz == dw == 0:
                        continue
                    count += 1 if get2(x+dx,y+dy,z+dz,w+dw,space) else 0
    #print("count:", count)
    a = get2(x,y,z,w,space)
    if a and count in [2,3]:
        return (True, False)
    if not a and count in [3]:
        return (True, True)
    return (False, a) # TODO kas qige?

#
#def prints(space):
#
#    for z in sorted(space[0][0].keys()):
#        print("z:", z)
#        for y in sorted(space[0].keys()):
#            for x in sorted(space.keys()):
#                print('#' if space[x][y][z] else '.', end="")
#            print()
#
for round in range(6):

    newspace = deepcopy(space)

    for x in range(lx - 1, ux + 2):
        for y in range(ly - 1, uy + 2):
            for z in range(lz - 1, uz + 2):
                for w in range(lw - 1, uw + 2):
                    (state, changed) = newstate2(x,y,z,w,space)
                    newspace.setdefault(x, {}).setdefault(y, {}).setdefault(z, {})[w] = state
                    if changed:
                        if state:
                            activated += 1
                        else:
                            activated -= 1

    #prints(newspace)
    lx -= 1
    ux += 1
    ly -= 1
    uy += 1
    lz -= 1
    uz += 1
    lw -= 1
    uw += 1
    space = newspace

print("Part2", activated)
