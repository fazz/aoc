
from aocd import data, post
from functools import reduce

input = data.split('\n')

def h(input):
    return reduce(lambda x, y: ((x + ord(y))*17)%256, input, 0)

seq = input[0].split(',')

r1 = sum(map(h, seq))

print("r1:", r1)

post.submit(r1, part="a", day=15)

boxes = [[] for x in range(256)]

def inbox(b, l):
    for (lb, f) in b:
        if lb == l:
            return b.index((lb, f))
    return -1

for e in seq:
    if '-' in e:
        label = e[:e.index('-')]
        focal = None
    else:
        label = e[:e.index('=')]
        focal = int(e[e.index('=')+1:])

    b = boxes[h(label)]
    i = inbox(b, label)

    if focal is None:
        if i >= 0:
            b.pop(i)
    else:
        if i >= 0:
            b[i] = (label, focal)
        else:
            b.append((label, focal))

r2 = 0
for (bi, bv) in enumerate(boxes):
    for (li, lv) in enumerate(bv):
        r2 += (bi+1)*(li+1)*lv[1]

print("r2:", r2)

post.submit(r2, part="b", day=15)
