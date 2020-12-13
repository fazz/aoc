import re
from functools import reduce
from collections import Counter

text_file = open("input10.txt", "r")

adapters = [0] + [(lambda a: int(a))(x.rstrip("\n\r")) for x in text_file.readlines()]
adapters.sort()
adapters.append(adapters[-1] + 3)

d = list(map(lambda a: adapters[a+1]-adapters[a], range(len(adapters)-1)))
c = Counter(d)

print("Part1:", c[3]*c[1])

def count(chain):
    r = set([tuple(chain)])
    for i in range(0, len(chain)-2):
        for j in range(i+1, len(chain)-1):
            if chain[j+1] - chain[i] <= 3:
                chain2 = list(chain)
                del chain2[j]
                r.add(tuple(chain2))
                r = r.union(count(chain2))
    return r

s = 0
m = []
for e in range(1, len(adapters)):
    if adapters[e] - adapters[e-1] == 3:
        m.append(len(count(adapters[s:e])))
        s = e

part2 = reduce(lambda a,b: a*b, m, 1)

print("Part2:", part2)
