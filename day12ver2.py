
from copy import deepcopy
from math import gcd
import itertools

position = {
    0: [10, 15, 7],
    1: [15, 10, 0],
    2: [20, 12, 3],
    3: [0, -3, 13]
}

position2 = {
    0: (-1, 0, 2),
    1: (2, -10, -7),
    2: (4, -8, 8),
    3: (3, 5, -1)
}

# Priit
position3 = {
    0: (1, 4, 4),
    1: (-4, -1, 19),
    2: (-15, -14, 12),
    3: (-17, 1, 10)
}

velocity = {
    0: [0, 0, 0],
    1: [0, 0, 0],
    2: [0, 0, 0],
    3: [0, 0, 0]
}

dimensions = {
    0: [10, 15, 20, 0, 0, 0, 0, 0]
}

origposition = deepcopy(position)
origvelocity = deepcopy(velocity)

loopsizes = []

unfound = set([0,1,2])

def sign(a, b):
    return (b-a) // (abs(b-a)) if a != b else 0

for loop in itertools.count():
    print(dimensions)
    pos = dimensions[0][0:4]
    vel = dimensions[0][4:8]
    for x in range(4):
        vel[x] -= len([z for z in pos if z < pos[x]])
        vel[x] += len([z for z in pos if z > pos[x]])
    for x in range(4):
        pos[x] += vel[x]

    pos.extend(vel)
    dimensions[0] = pos

    if vel == [0, 0, 0, 0]:
        print("Loops:", loop+1)
        break