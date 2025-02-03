import datetime
from copy import deepcopy, copy
from itertools import product
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

input = [int(x.rstrip(" \n\r")) for x in open("input20.txt", "r")]

statesize = len(input)

def calc(numbers, indexes):

    for nn in range(len(numbers)):

        i = indexes.index(nn)

        n = numbers.pop(i)
        indexes.pop(i)

        newindex = (i + n) % (statesize-1)

        numbers.insert(newindex, n)
        indexes.insert(newindex, nn)

    return (numbers, indexes)

indexes = list(range(len(input)))

(numbers, indexes) = calc(copy(input), indexes)

zi = numbers.index(0)

print("Part 1:", numbers[(zi+1000)%statesize]+numbers[(zi+2000)%statesize]+numbers[(zi+3000)%statesize])

key = 811589153

numbers = [x*key for x in input]

indexes = list(range(len(numbers)))

for round in range(10):
    (numbers, indexes) = calc(numbers, indexes)

zi = numbers.index(0)

print("Part 2:", numbers[(zi+1000)%statesize]+numbers[(zi+2000)%statesize]+numbers[(zi+3000)%statesize])


end = datetime.datetime.now()
print("Milliseconds:", (end-start_time).seconds*1000 + (end-start_time).microseconds // 1000)
