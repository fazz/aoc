
from queue import PriorityQueue

text_file = open("input20.txt", "r")
lines = text_file.readlines()

area = {}
distances = {}

alphas = []
portals = {}
portalpoints = {}

W = '#'
F = '.'
S = '0'
O = 'O'

def ga(x, y):
    if y in area:
        if x in area[y]:
            return area[y][x]
    return S

maxy = 0
maxx = 0

# Collect 
for y in range(len(lines)):
    x = 0
    for c in lines[y]:
        if c.isalpha():
            alphas.append((y,x))
        area.setdefault(y, {})[x] = c if c != ' ' else S
        maxx = max(maxx, x)
        x += 1
    maxy = max(maxy, y)

# Determine portals
for y in range(maxy+1):
    for x in range(maxx+1):
        c = ga(x,y)
        if not c.isalpha(): 
            continue
        d = (1, 0)
        for z in range(4):
            c2 = ga(x+d[0], y+d[1])
            if c2 == F:
                portalpoint = (x+d[0], y+d[1])
                d = (-d[0], -d[1])
                c3 = ga(x+d[0], y+d[1])
                if sum(d) < 0:
                    portal = c3+c
                else:
                    portal = c+c3

                portalo = (portal, O)
                portali = (portal, 'i')

                #distances.setdefault(portalo, {})[portali] = 1
                #distances.setdefault(portali, {})[portalo] = 1

                if x == 1 or y == 1 or x == maxx-2 or y == maxy-1:
                    portal = portalo
                else:
                    portal = portali
                
                portals[portal] = portalpoint
                portalpoints[portalpoint] = portal
                    
                break
            d = (-d[1], d[0])

# BFS for relating portals

def bfs(portal):
    result = []
    visited = {}

    x = portals[portal][0]
    y = portals[portal][1]

    d = (0, 1)
    queue = [(x,y,0)]
    visited[(x,y)] = True

    while len(queue):
        p = queue.pop(0)
        x = p[0]
        y = p[1]

        if p[2] != 0 and (x,y) in portalpoints:
            result.append((portalpoints[(x,y)], p[2]))

        for z in range(4):
            if ga(x+d[0], y+d[1]) == F and (x+d[0], y+d[1]) not in visited:
                queue.append((x+d[0], y+d[1], p[2]+1))
                visited[(x+d[0], y+d[1])] = True

            d = (-d[1], d[0])

    return result


for p in portals.keys():
    distances.setdefault(p, {})
    result = bfs(p)
    for r in result:
        distances[p][r[0]] = r[1]
        distances.setdefault(r[0], {})[p] = r[1]


# Part 1
# Djikstra shortest path AA to ZZ

def part1():
    print("Djikstra 1")

    portalnames = set(portals.keys())
    dist = {}
    dist[('AA', O)] = 0
    prev = {}
    prev[('AA', O)] = None

    while True:
        if len(portalnames) == 0:
            break
        mind = 9999999999999
        minp = None
        for p in portalnames:
            if p in dist and dist[p] < mind:
                mind = dist[p]
                minp = p
        if minp == None:
            break # The graph is broken or exhausted
        portalnames.remove(minp)
        if minp == ('ZZ', O):
            break

        for p in distances[minp]:
            alt = dist[minp] + distances[minp][p]
            if p not in dist or alt < dist[p]:
                dist[p] = alt
                prev[p] = minp

    print('Result 1:', dist[('ZZ', O)])


# Part 2
# Djikstra shortest path AA to ZZ

def neighbours(portal):
    directs = distances[portal[1]].keys()
    cost = portal[0]
    pt = portal[1]
    level = portal[2]

    #print("Directs:", directs)
    if level == 0:
        directs = [p for p in directs if p[1] == 'i' or p[0] == 'AA' or p[0] == 'ZZ']
    else:
        directs = [p for p in directs if p[0] != 'AA' and p[0] != 'ZZ']

    directs = [(cost+distances[portal[1]][p], p, level) for p in directs]

    # Add intra-dimensional stuff
    if pt[1] == 'i':
        directs.append((cost+1, (portal[1][0], O), level+1))
    elif pt[0] != 'AA' and pt[0] != 'ZZ':
        directs.append((cost+1, (portal[1][0], 'i'), level-1))

    return directs


print("UCS")

queue = PriorityQueue()

# Dist, portal, level
queue.put((0, ('AA', O), 0))

# (portal, level)
visited = set()

dist = 0

result = 0

while True:
    if queue.empty():
        #print("Error no Q")
        break

    p = queue.get()
    #print("Got from Q:", p)
    if p[1] == ('ZZ', O):
        result = p[0]
        break

    visited.add((p[1], p[2]))

    nbh = neighbours(p)

    for n in nbh:
        if (n[1], n[2]) in visited:
            continue
        queue.put(n)
        #print("Put to Q:", n)

print('Result 2', result)
