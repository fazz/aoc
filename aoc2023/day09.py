
from aocd import data, post
from functools import reduce

input = data.split('\n')

r1 = 0
r2 = 0

for l in input:
    l = tuple(map(int, l.split()))

    stack = [l]

    while sum(stack[-1]) != 0:
        stack.append([stack[-1][x+1] - stack[-1][x] for x in range(len(stack[-1])-1)])

    r1 += sum([r[-1] for r in stack])
    r2 += reduce(lambda o, t: t-o, [r[0] for r in reversed(stack[:-1])], 0)

print("r1:", r1)

post.submit(r1, part="a", day=9)

print("r2:", r2)

post.submit(r2, part="b", day=9)
