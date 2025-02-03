
import sys
sys.path.insert(0, "../aoc2023")

from aocd import data, post
from operator import xor
from collections import defaultdict, deque

input = tuple(map(int, data.split('\n')))

def next(v):
    v = (v ^ (v<<6)) & (2**24)-1
    v = (v ^ (v>>5)) & (2**24)-1
    v = (v ^ (v<<11)) & (2**24)-1

    return v

sequence = defaultdict(int)

r1 = 0
for i in input:
    seq = deque()
    prev = None
    seen = set()
    for c in range(2000):
        i = next(i)
        if prev is not None:
            seq.append((i % 10) - prev)
            if c > 4:
                seq.popleft()
            k = tuple(seq)
            if k not in seen:
                sequence[k] += i % 10
                seen.add(k)
        prev = i % 10
    r1 += i

r2 = max(sequence.values())

print("r1:", r1)
print("r2:", r2)

post.submit(r1, part="a", day=22)
post.submit(r2, part="b", day=22)
