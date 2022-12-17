import datetime
from copy import deepcopy, copy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

lines = [x.rstrip(" \n\r") for x in open("input17.txt", "r")]

input = list(lines[0])

shapes = {
    0: set([(0, 0), (1, 0), (2, 0), (3, 0)]),
    1: set([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
    2: set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    3: set([(0, 0), (0, 1), (0, 2), (0, 3)]),
    4: set([(0, 0), (0, 1), (1, 0), (1, 1)])
}

def calc(rockcount, jetnumber, bottomshape, detectrepeat):
    shapen = 0

    occupied = set()

    for x in range(7):
        occupied.add((x,bottomshape[x]))

    bottom = list(bottomshape)

    statedata = {}

    for x in range(rockcount * (10 if detectrepeat else 1)):
        shape = copy(shapes[shapen%5])

        if len(occupied) == 0:
            llc = (2, 4)
        else:
            llc = (2, max([z[1] for z in occupied]) + 4)

        (x, y) = llc

        shape = set([(z[0] + x, z[1] + y) for z in shape])

        falling = True

        while falling:
            direction = -1 if input[jetnumber%len(input)] == '<' else 1
            jetnumber += 1

            newshape = set([(z[0] + direction, z[1]) for z in shape])

            xss = [z[0] for z in newshape]

            if min(xss) >= 0 and max(xss) <= 6 and len(newshape.intersection(occupied)) == 0:
                shape = newshape

            newshape = set([(z[0], z[1] - 1) for z in shape])

            if len(newshape.intersection(occupied)) == 0:
                shape = newshape
            else:
                occupied = occupied.union(shape)
                falling = False

                if detectrepeat:

                    for point in shape:
                        bottom[point[0]] = max(point[1], bottom[point[0]])

                    height = max(bottom)

                    om = min(bottom)
                    bottomshape = tuple([z-om for z in bottom])

                    if bottomshape in statedata:
                        data = statedata[bottomshape]

                        if jetnumber%len(input) == data[1]%len(input):

                            firstroundrocks = data[2]
                            firstroundheight = data[0]

                            roundheight = height - data[0]

                            roundsizeinrocks = shapen+1 - data[2] # on see õige?
                            jetnumber = jetnumber%len(input)

                            return (firstroundrocks, firstroundheight, roundheight, roundsizeinrocks, jetnumber, bottomshape)

                    else:
                        if shapen%5 == 0:
                            statedata[bottomshape] = (height, jetnumber, shapen+1)

        shapen += 1

    return max([z[1] for z in occupied])


print("Part 1:", calc(2022, 0, (0, 0, 0, 0, 0, 0, 0), False))

####################################

(firstroundrocks, firstroundheight, roundheight, roundsizeinrocks, jetnumber, bottomshape) = calc(2022, 0, (0, 0, 0, 0, 0, 0, 0), True)

rockcount = (1000000000000-firstroundrocks)%roundsizeinrocks

h = calc(rockcount, jetnumber, bottomshape, False)

print("Part 2:", firstroundheight + ((1000000000000-firstroundrocks)//roundsizeinrocks)*roundheight + h - max(bottomshape) - 1)

end = datetime.datetime.now()

print("Milliseconds:", (end-start_time).seconds*1000 + (end-start_time).microseconds // 1000)
