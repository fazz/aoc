
from collections import defaultdict

input = 325489

def br(level):
    if level == 0:
        return 1
    else:
        return level*2*4 + br(level-1)

level = 0
brv = 0

while True:
    brv = br(level)
    if brv >= input:
        break
    level += 1

sl = level*2

result1 = level + min([abs(input-x) for x in [brv-(sl//2), brv-1*sl-(sl//2), brv-2*sl-(sl//2), brv-3*sl-(sl//2)]])

print("Part 1:", result1)

map = defaultdict(lambda: 0)
map[(0,0)] = 1

x = 1
y = 0
dir = (0, 1)
level = 1

result2 = 0
while True:
    v = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            v += map[(x+i, y+j)]
    map[(x,y)] = v
    if v > input:
        result2 = v
        break

    if x == level and y == -level:
        level += 1
    elif max(abs(x+dir[0]), abs(y+dir[1])) > level:
        dir = (-dir[1], dir[0])

    (x,y) = (x+dir[0], y+dir[1])

print("Part 2:", result2)

