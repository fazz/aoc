
from copy import deepcopy
from itertools import compress

text_file = open("input05.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

stacks1 = {}

movestart = 0
while True:
    l = lines[movestart]
    if l == "":
        break
    for j in range(len(l)):
        if l[j] >= 'A' and l[j] <= 'Z':
            p = (j - 1) // 4 + 1
            if not p in stacks1:
                stacks1[p] = []
            stacks1[p].append(l[j])
    movestart += 1

stacks2 = deepcopy(stacks1)

def move(stacks, amt, pile, src, dst):
    for _ in range(amt//pile):
        tmp = stacks[src][0:pile]
        stacks[src] = stacks[src][pile:]
        stacks[dst] = tmp + stacks[dst]
    return stacks

for l in lines[movestart+1:]:
    (amt, src, dst) = tuple(map(int, compress(l.split(' '), [0, 1, 0, 1, 0, 1])))

    stacks1 = move(stacks1, amt, 1, src, dst)
    stacks2 = move(stacks2, amt, amt, src, dst)

result1 = ""
result2 = ""

for x in sorted(stacks1.keys()):
    result1 += stacks1[x][0]
    result2 += stacks2[x][0]

print("Part 1:", result1)
print("Part 2:", result2)
