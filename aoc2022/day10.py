
from copy import deepcopy
from itertools import compress
from functools import reduce
import operator
from collections import defaultdict

lines = [x.rstrip("\n\r") for x in open("input10.txt", "r")]

clock = 1
result1 = 0
register = 1
screen = defaultdict(lambda: defaultdict(lambda: ' '))

def tick(clock, register, screen):
    (y, x) = ((clock-1) // 40, (clock-1) % 40)
    if x in (register-1, register, register+1):
        screen[y][x] = '#'
    return clock*register if (clock - 20) % 40 == 0 else 0

for l in lines:
    i = l.split(' ')
    for _ in range(len(i)):
        result1 += tick(clock, register, screen)
        clock += 1
    if len(i) == 2:
        register += int(i[1])

print("Part 1:", result1)

print("Part 2:")

for y in range(6):
    for x in range(40):
        print(screen[y][x], end='')
    print()

