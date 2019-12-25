
from queue import PriorityQueue


filename = "input182.txt"
#filename = "input182test72.txt"

text_file = open(filename, "r")
lines = text_file.readlines()

area = {}
distances = {}

keys = {}
gates = {}
starts = {}

W = '#'
F = '.'
SM = '@'

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
        elif c == SM:
            starts[str(len(starts))] = (x,y)

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
        (x,y) = starts[point]

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
            if (np in (F, '0', '1', '2', '3', SM) or isgate(np) or iskey(np)) and (x+d[0], y+d[1]) not in visited:

                queue.append((x+d[0], y+d[1], p[2]+1, np, gotw))
                visited[(x+d[0], y+d[1])] = True

            d = (-d[1], d[0])

    # (point type, dist, gotw)
    return result


for p in list(gates.keys()) + list(keys.keys()) + list([str(x) for x in range(4)]):
    distances.setdefault(p, {})
    result = bfs(p)
    for r in result:
        # dist, gotw
        distances[p][r[0]] = (r[1], r[2])
        distances.setdefault(r[0], {})[p] = (r[1], r[2])

# Part 2

print("Process")

# tuple of traversed keys -> distance, keyset
mindistances = {}

queue = PriorityQueue()

# set + last -> dist, keyset
mindistances[(('0', ), ('1', ), ('2', ), ('3', ))] = (0, set(['0', '1', '2', '3']))

queue.put((0, (('0', ), ('1', ), ('2', ), ('3', ))))

while True:
    if queue.empty():
        print("Error Q empty")
        break

    # dist, path
    q = queue.get()
    dist = q[0]
    # tuple
    mdt = q[1]

    mdv = mindistances.setdefault(mdt, 999999999999999)

    passed = set(mdt[0]).union(mdt[1]).union(mdt[2]).union(mdt[3])

    for movingrobot in range(4):
        last = mdt[movingrobot][-1]
        dst = distances[last]
        
        for d in dst:
            if d in passed:
                continue

            if isgate(d):
                continue
            
            gotw = dst[d][1]
            if not set([gatekey(x) for x in gotw]).issubset(passed):
                continue

            newdist = dist + dst[d][0]

            kt = list(mdt)
            kt[movingrobot] = tuple(sorted(mdt[movingrobot])) + (d, )
            kt = tuple(kt)

            currentmin = mindistances.setdefault(kt, (99999999999999999, set()))[0]
            if currentmin > newdist:
                mindistances[kt] = (newdist, passed.union([d]))

                queue.put((newdist, kt))


result = min([x[0] for x in filter(lambda x: len(x[1]) == keycount + 4, mindistances.values())])
print("Result 2:", result)
