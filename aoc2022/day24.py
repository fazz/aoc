
from heapq import *

lines = [x.rstrip(" \n\r") for x in open("input24.txt", "r")]

(miny, maxy, minx, maxx) = (1, len(lines)-2, 1, len(lines[0])-2)

start_pos = (lines[0].index('.'), miny-1)
end_pos = (lines[-1].index('.'), maxy+1)

bd = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}

blizzardminuteh = {0: {}}
blizzardminutev = {0: {}}

for li in range(len(lines)):
    for ci in range(len(lines[li])):
        if lines[li][ci] not in ('.', '#'):
            if lines[li][ci] in ('<', '>'):
                blizzardminuteh[0][(ci, li)] = bd[lines[li][ci]]
            else:
                blizzardminutev[0][(ci, li)] = bd[lines[li][ci]]

def updateblizzard(minute):
    p = max(blizzardminuteh)%maxx

    for m in range(p+1, minute%maxx+1):
        ns = {}
        blizzardminuteh[m] = ns
        for b,d in blizzardminuteh[0].items():
            ns[((b[0]+d[0]*m-1)%maxx+1, b[1])] = 1

    p = max(blizzardminutev)%maxy

    for m in range(p+1, minute%maxy+1):
        ns = {}
        blizzardminutev[m] = ns
        for b,d in blizzardminutev[0].items():
            ns[(b[0], (b[1]+d[1]*m-1)%maxy+1)] = 1

def getdirections(minute, x, y):
    bzrdsh = blizzardminuteh[minute%maxx]
    bzrdsv = blizzardminutev[minute%maxy]

    ret = []
    for (nx, ny) in ((x, y), (-1+x, y), (1+x, y), (x, -1+y), (x, 1+y)):
        if (nx >= 1 and nx <= maxx and ny >= 1 and ny <= maxy and (nx, ny) not in bzrdsh and (nx, ny) not in bzrdsv) or (nx, ny) == end_pos or (nx, ny) == start_pos:
            ret.append((minute, nx, ny))

    return ret

updateblizzard(699)

q = []

heappush(q, (0, 0, *start_pos))

result1 = None
result2 = None
targets = [end_pos, start_pos, end_pos]

visited = set()

while len(q) > 0:
    curr = heappop(q)

    (_, minute, x, y) = curr

    if (x,y) == targets[0]:
        targets.pop(0)
        if result1 == None:
            result1 = minute
        if len(targets) == 0:
            result2 = minute
            break
        q = []
        visited = set(curr)

    free = getdirections(minute+1, x, y)

    for step in free:
        predict = minute + 1 + abs(step[1]-targets[0][0]) + abs(step[2]-targets[0][1])

        if step not in visited:
            visited.add(step)
            heappush(q, (predict, *step))

print("Part 1:", result1, 242)
print("Part 2:", result2, 720)

