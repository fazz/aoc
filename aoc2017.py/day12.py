
from collections import defaultdict

text_file = open("input12.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

collect = defaultdict(lambda: set())

for l in lines:
    l = l.replace(',', '').replace(' <->', '')
    conn = tuple(map(int, l.split(' ')))
    collect[conn[0]].update(conn)

visited = collect[0]

def calc(k, visited):

    ret = set(visited)

    for v in set(collect[k]).difference(visited):
        ret.add(v)
        nv = calc(v, ret)
        ret.update(nv)

    return ret

visited = calc(0, {0})
print("Part 1:", len(visited))

candidates = set(range(max(collect.keys())+1))

result2 = 0

while len(candidates) > 0:
    x = tuple(candidates)[0]
    visited = calc(x, {x})
    result2 += 1
    candidates = candidates.difference(visited)

print("Part 2:", result2)
