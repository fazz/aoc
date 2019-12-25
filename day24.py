
from copy import deepcopy

filename = "input24.txt"

text_file = open(filename, "r")
lines = text_file.readlines()

area = {}
bugs = set()

for l in range(len(lines)):
    for c in range(len(lines[l])):
        if lines[l][c] == '#':
            area.setdefault(l, {})[c] = 1
            bugs.add((c,l,0))
        elif lines[l][c] == '.':
            area.setdefault(l, {})[c] = 0

print("")

for y in range(5):
    for x in range(5):
        print(area[y][x], end='')
    print("")

print("")

def ga(x,y):
    if y in area:
        if x in area[y]:
            return area[y][x]
    return 0

def izbug(x,y,l):
    return (x, y, l) in bugs
    
def count(x,y):
    return ga(x-1, y) + ga(x+1, y) + ga(x, y-1) + ga(x, y+1)

def adj(x,y,l):
    for d in ((1,0), (-1, 0), (0, 1), (0, -1)):
        (x1, y1) = (x+d[0], y+d[1])

        if x1 in (0,1,2,3,4) and y1 in (0,1,2,3,4) and (x1,y1) != (2,2):
            yield (x1,y1,l)
            continue
        if (x1 in (-1,5) and y1 in (0,1,2,3,4)) or (y1 in (-1,5) and x1 in (0,1,2,3,4)):
            if x1 == -1:
                x1 = 1
                y1 = 2
            elif x1 == 5:
                x1 = 3
                y1 = 2
            elif y1 == -1:
                x1 = 2
                y1 = 1
            elif y1 == 5:
                x1 = 2
                y1 = 3
            yield(x1, y1, l-1)
            continue
        if (x1,y1) == (2,2):
            if d[0] == -1:
                # x =4, y rot
                for z in range(5):
                    yield(4,z,l+1)
            elif d[0] == 1:
                # x =0, y rot
                for z in range(5):
                    yield(0,z,l+1)
            elif d[1] == 1:
                # y= 0, x rot
                for z in range(5):
                    yield(z,0,l+1)
            elif d[1] == -1:
                # y = 4, x rot
                for z in range(5):
                    yield(z,4,l+1)

            continue

        raise RuntimeError("WTF")

    return


def count2(x,y,l):
    count = 0
    spaces = set()
    for (x1, y1, l1) in adj(x,y,l):
        iz = izbug(x1, y1, l1)
        #print("count2:", (x,y,l), (x1, y1, l1), iz)
        if iz:
            count += 1
        else:
            spaces.add((x1, y1, l1))
    return (count, spaces)


bd = set()

while True:
    newarea = {}
    newbd = 0
    for y in range(5):
        for x in range(5):
            c = count(x, y)
            if c == 1:
                newarea.setdefault(y, {})[x] = 1
                newbd += 2**(y*5+x)
            elif c == 2:
                v = (area[y][x] + 1) % 2
                newarea.setdefault(y, {})[x] = v
                if v == 1:
                    newbd += 2**(y*5+x)
            else:
                newarea.setdefault(y, {})[x] = 0
    if newbd in bd:
        result = newbd
        break
    bd.add(newbd)
    area = newarea

print("Result 1", result)
print("Bugs", len(bugs))

for i in range(200):
    print("i:", i, len(bugs))
    newbugs = set()
    spaces = set()
    for (bx, by, bl) in bugs:
        (c, spaces) = count2(bx, by, bl)
        #print("Bug", bx, by, bl, c, spaces)
        if c == 1:
            newbugs.add((bx, by, bl))

        for (sx, sy, sl) in spaces:
            (c, s) = count2(sx, sy, sl)
            if c in (1,2):
                newbugs.add((sx, sy, sl))
    
    bugs = newbugs
    #print("Bugs", bugs)


print("Result 2", len(bugs))

