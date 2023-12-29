
from aocd import data, post

input = data.split('\n')

r1 = 0

counts = {x: 1 for x in range(len(input))}

for li in range(len(input)):
    l = input[li]

    (pr, n) = l.split(': ')
    (w, h) = n.split(' | ')

    w = set(map(int, w.split()))
    h = set(map(int, h.split()))

    c = len(w.intersection(h))

    if c > 0:
        r1 += 2 ** (c-1)

    for x in range(li+1, li+1+c):
        counts[x] += counts[li]

post.submit(r1, part="a", day=4)

r2 = sum(counts.values())

post.submit(r2, part="b", day=4)
