

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
                if c == 'E':
                    print(d, x, y)
                portalpoint = (x+d[0], y+d[1])
                d = (-d[0], -d[1])
                c3 = ga(x+d[0], y+d[1])
                if sum(d) < 0:
                    portal = c3+c
                else:
                    portal = c+c3

                i = portal + 'i'
                distances.setdefault(portal, {})[i] = 1
                distances.setdefault(i, {})[portal] = 1
                if not (x == 1 or y == 1 or x == 133 or y == 125):
                    portal = i
                
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
    print("BFS", p)
    distances.setdefault(p, {})
    result = bfs(p)
    for r in result:
        distances[p][r[0]] = r[1]
        distances.setdefault(r[0], {})[p] = r[1]


# Djikstra shortest path AA to ZZ

print("Djikstra")

portalnames = set(portals.keys())
dist = {}
dist['AA'] = 0
prev = {}
prev['AA'] = None

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
    if minp == 'ZZ':
        break

    for p in distances[minp]:
        alt = dist[minp] + distances[minp][p]
        if p not in dist or alt < dist[p]:
            dist[p] = alt
            prev[p] = minp

print('Result 1', dist['ZZ'])
