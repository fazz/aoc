
from copy import deepcopy
from math import gcd
import itertools

position = {
    0: (10, 15, 7),
    1: (15, 10, 0),
    2: (20, 12, 3),
    3: (0, -3, 13)
}

position2 = {
    0: (-1, 0, 2),
    1: (2, -10, -7),
    2: (4, -8, 8),
    3: (3, 5, -1)
}

velocity = {
    0: (0, 0, 0),
    1: (0, 0, 0),
    2: (0, 0, 0),
    3: (0, 0, 0)
}

origposition = deepcopy(position)
origvelocity = deepcopy(velocity)

def dimensions(p, v):
    result = {}
    for a in range(3):

        d = tuple([p[m][a] for m in range(4)] + [v[m][a] for m in range(4)])

        result[a] = d

    return result

origdimensions = dimensions(position, velocity)

loopsizes = {}

for loop in itertools.count():

    dim = dimensions(position, velocity)

    for d in range(3):
        if dim[d] == origdimensions[d] and loop > 0:
            loopsizes.setdefault(d, loop)

    if len(loopsizes) == 3:
        break

    # Gravity
    posdiffs = {}
    for moon in range(4):
        for moon2 in range(moon+1, 4):
            # for moon
            diff = []
            for c in zip(position[moon], position[moon2]):
                d = 0
                if c[1] != c[0]:
                    d = (c[1]-c[0]) // (abs(c[1]-c[0]))
                diff.append(d)
            posdiffs.setdefault(moon, {})[moon2] = tuple(diff)
            posdiffs.setdefault(moon2, {})[moon] = tuple([-x for x in diff])

    # Velocity
    for m in posdiffs.keys():
        v = tuple([sum(x) for x in zip(velocity[m], *posdiffs[m].values())])
        velocity[m] = v

    # Position
    for m in range(4):
        position[m] = tuple([sum(x) for x in zip(position[m], velocity[m])])

    if loop == 1000-1:
        result = 0
        for m in range(4):
            result += sum([abs(x) for x in position[m]]) * sum([abs(x) for x in velocity[m]])

        print(result)

print(loopsizes)

def lcm(a, b):
    return a * b // gcd(a, b)

ls = tuple(loopsizes.values())

print(ls[0]*ls[1]*ls[2])
print(lcm(ls[0], lcm(ls[1], ls[2])))
