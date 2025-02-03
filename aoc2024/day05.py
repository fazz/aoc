
from aocd import data, post
from collections import defaultdict
from functools import cmp_to_key

(rules, records) = map(lambda x: x.split('\n'), data.split('\n\n'))

l2r = defaultdict(list)

for rr in rules:
    (l, r) = map(int, rr.split('|'))
    l2r[l].append(r)

def compare(a, b):
    return -1 if b in l2r[a] else 1

r1 = 0
r2 = 0
for rec in records:
    rec = list(map(int, rec.split(',')))
    rec2 = sorted(rec, key=cmp_to_key(compare))

    if rec2 == rec:
        r1 += rec[len(rec)//2]
    else:
        rec2 = sorted(rec, key=cmp_to_key(compare))
        r2 += rec2[len(rec2)//2]


post.submit(r1, part="a", day=5)
post.submit(r2, part="b", day=5)
