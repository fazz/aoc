
text_file = open("input11.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

path = lines[0].split(',')

dirs = {
    "n":  {0: (0, -1, 0),  1: (0, -1, 0)},
    "ne": {0: (0, 0, 1),   1: (1, -1, 1)},
    "se": {0: (0, 1, 1),  1: (1, 0, 1)},
    "s":  {0: (0, 1, 0),   1: (0, 1, 0)},
    "sw": {0: (-1, 1, 1), 1: (0, 0, 1)},
    "nw": {0: (-1, 0, 1),  1: (0, -1, 1)}
}

(x,y,z) = (0,0,0)

collect = []

for m in path:
    d = dirs[m]
    (x,y,z) = (x + d[z][0], y + d[z][1], (z + d[z][2]) % 2)
    collect.append((x,y,z))

def dist(x,y,z):
    dx = abs(x) - (z if x < 0 else 0)
    dy = abs(y) - (z if y > 0 else 0)
    return dx+dy+z

print("Part 1:", dist(x,y,z))

result2 = 0

for c in collect:
    d = dist(*c)
    if d > result2:
        result2 = d

print("Part 2:", result2)
