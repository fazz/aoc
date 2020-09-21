
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

origposition = deepcopy(position)
origvelocity = deepcopy(velocity)

loopsizes = []

unfound = set([0,1,2])

def sign(a, b):
    return (b-a) // (abs(b-a)) if a != b else 0

for loop in itertools.count():

    remove = set()
    for d in unfound:
        if velocity[0][d] == 0:
            if tuple([v[d] for v in velocity.values()]) == (0,0,0,0) and loop > 0:
                print(position, velocity)
                loopsizes.append(loop)
                remove.add(d)
    
    for r in sorted(remove, reverse = True):
        for k in position.keys():
            velocity[k].pop(r)
            position[k].pop(r)
        unfound.remove(max(unfound))

    if len(loopsizes) == 3:
        break

    # Velocity
    for moon in range(4):
        for moon2 in range(moon+1, 4):
            diff = [sign(c[0], c[1]) for c in zip(position[moon], position[moon2])]
            velocity[moon] = [d[0] + d[1] for d in zip(velocity[moon], diff)]
            velocity[moon2] = [d[0] - d[1] for d in zip(velocity[moon2], diff)]

    # Position
    for m in range(4):
        position[m] = [sum(x) for x in zip(position[m], velocity[m])]

    if loop == 1000-1:
        result = 0
        for m in range(4):
            result += sum([abs(x) for x in position[m]]) * sum([abs(x) for x in velocity[m]])

        print(result)

print(loopsizes)

def lcm(a, b):
    return a * b // gcd(a, b)

ls = loopsizes

print(ls[0]*ls[1]*ls[2])
#print(lcm(ls[0], lcm(ls[1], ls[2])))
