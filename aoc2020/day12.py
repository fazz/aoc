
import copy
from itertools import product

text_file = open("input12.txt", "r")

moves = [x.rstrip("\n\r") for x in text_file.readlines()]

def move(c, s, pos, direction):
    if c != 'F':
        s = 0
    return (pos[0] + s*direction[0], pos[1] + s*direction[1])

def wpdelta(c, s, direction):
    if c in ['R', 'L', 'F']:
        return (0, 0)
    if c == 'N':
        return (0, s)
    if c == 'S':
        return (0, -s)
    if c == 'E':
        return (s, 0)
    if c == 'W':
        return (-s, 0)

def turn(c, s, direction):
    times = s // 90

    if c in ['R', 'L']:
        for i in range(times):
            if c == 'R':
                direction = (direction[1], -1*direction[0])
            elif c == 'L':
                direction = (-1*direction[1], direction[0])

    return direction

def calc(dx, dy, movingwp):
    direction = (dx, dy)
    pos = (0, 0)

    for m in moves:
        c = m[0]
        s = int(m[1:])

        pos = move(c, s, pos, direction)

        wpd = wpdelta(c, s, direction)

        direction = turn(c, s, direction)

        if movingwp:
            direction = (direction[0]+wpd[0], direction[1]+wpd[1])
        else:
            pos = (pos[0]+wpd[0], pos[1]+wpd[1])

    return abs(pos[0])+abs(pos[1])

print("Part1:", calc(1, 0, False))
print("Part2:", calc(10, 1, True))
