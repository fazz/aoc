
from itertools import filterfalse

x = -1
input = [29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,409,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17,13,19,x,x,x,23,x,x,x,x,x,x,x,353,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41]

earliest = 1000511

times = list(filterfalse(lambda z: z == x, input))

minb = None
mindiff = 999999999999
for t in times:
    mult = earliest // t
    deptime = t * ((earliest // t)+1)
    diff = deptime - earliest
    if diff < mindiff:
        mindiff = diff
        minb = t

print("Part1:", minb*mindiff)

times2 = {}
for i in range(len(input)):
    if input[i] != x:
        times2[input[i]] = i

first = 0

add = input[0]
addset = set([add])
found = False
count = 0
while not found:
    found = True
    for v in set(times2.keys()).difference(addset):
        count += 1
        if (first + times2[v]) % v != 0:
            found = False
            break
        else:
            add *= v
            addset.add(v)
    if not found:
        first += add

print("Part2:", first, count)
