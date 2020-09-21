
from queue import PriorityQueue


filename = "input18.txt"
#filename = "input18test86.txt"
#filename = "input18test136.txt"

text_file = open(filename, "r")
lines = text_file.readlines()

area = {}
distances = {}

keys = {}
gates = {}
start = None

W = '#'
F = '.'
S = '@'

def ga(x, y):
    if y in area:
        if x in area[y]:
            return area[y][x]
    return S

def iskey(c):
    return ord(c) >= ord('a') and ord(c) <= ord('z')

def isgate(c):
    return ord(c) >= ord('A') and ord(c) <= ord('Z')

def gatekey(c):
    return chr(ord(c)-ord('A')+ord('a'))

# Collect 
for y in range(len(lines)):
    for x in range(len(lines[y])):

        c = lines[y][x]

        if iskey(c):
            keys[c] = (x,y)
        elif isgate(c):
            gates[c] = (x,y)
        elif c == S:
            start = (x,y)

        area.setdefault(y, {})[x] = c

keycount = len(keys)
print("Keys:", keycount)

# BFS for relating portals

def bfs(point):
    result = []
    visited = {}

    if point in gates:
        (x,y) = gates[point]
    elif point in keys:
        (x,y) = keys[point]
    else:
        (x,y) = start


    d = (0, 1)
    # x, y, 0, pointname, gatesOTW
    queue = [(x,y,0,point,[])]
    visited[(x,y)] = True

    while len(queue):
        p = queue.pop(0)
        x = p[0]
        y = p[1]

        c = p[3]

        gotw = p[4]

        if p[2] != 0 and isgate(c):
            gotw = gotw + [c]

        if p[2] != 0 and (isgate(c) or iskey(c)):
            result.append((c, p[2], gotw))

        for z in range(4):
            np = ga(x+d[0], y+d[1])
            if (np in (F, S) or isgate(np) or iskey(np)) and (x+d[0], y+d[1]) not in visited:

                queue.append((x+d[0], y+d[1], p[2]+1, np, gotw))
                visited[(x+d[0], y+d[1])] = True

            d = (-d[1], d[0])

    # (point type, dist, gotw)
    return result


for p in [S] + list(gates.keys()) + list(keys.keys()):
    distances.setdefault(p, {})
    result = bfs(p)
    for r in result:
        # dist, gotw
        distances[p][r[0]] = (r[1], r[2])
        distances.setdefault(r[0], {})[p] = (r[1], r[2])

# Part 1

print("Process")
# Target: those equal
allkeys = set(keys.keys())

# tuple of traversed keys -> distance, path
mindistances = {}

queue = PriorityQueue()


# set + last -> dist, path
mindistances[tuple(S)] = (0, [S])

queue.put((0, (S, )))


while True:
    if queue.empty():
        print("Error Q empty")
        break

    q = queue.get()
    dist = q[0]
    md = q[1]

    mdv = mindistances.setdefault(md, 999999999999999)

    last = md[-1]
    md = set(md)
    dst = distances[last]
    for d in dst:

        #
        # 1. Teada on path ja tema viimane element.
        # 2. Leia distants, mis toob selle elemendini läbi hulga, kuhu ta kuulub
        # 
        if d in md:
            # already visited
            continue

        if isgate(d):
            continue
        
        gotw = dst[d][1]
        if not set([gatekey(x) for x in gotw]).issubset(md):
            continue

        newdist = dist + dst[d][0]
        kt = tuple(sorted(md)) + (d, )

        currentmin = mindistances.setdefault(kt, (99999999999999999, []))[0]
        if currentmin > newdist:
            mindistances[kt] = (newdist, kt)

            #if kt == tuple(sorted(allkeys.union({S}))):
            #print("Full:", newdist, kt)

            queue.put((newdist, kt))



result = min([x[1][0] for x in filter(lambda x: len(x[0]) == keycount + 1, mindistances.items())])

print(result)

# 4606 liiga kõrge
# 4402 liiga kõrge
# 4368 on vale
# 4290 on vale
# 4252 on vale

# 4258??
# 4252
