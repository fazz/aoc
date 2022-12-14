
from copy import deepcopy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict

lines = [eval(y) for y in [x.rstrip(" \n\r") for x in open("input13.txt", "r")] if len(y) > 0]

def compare(vv1, vv2):
    for i in range(min(len(vv1), len(vv2))):
        (v1, v2) = (vv1[i], vv2[i])
        r = 0
        if isinstance(v1, int) and isinstance(v2, int):
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        else:
            if isinstance(v1, int):
                v1 = [v1]
            elif isinstance(v2, int):
                v2 = [v2]
            r = compare(v1, v2)
        if r != 0:
            return r

    if len(vv1) != len(vv2):
        return -1 if len(vv1) < len(vv2) else 1
    return 0

result1 = reduce(lambda r, x: r + (x+1 if compare(lines[x*2], lines[x*2+1]) < 0 else 0), range((len(lines)+1)//2), 0)

print("Part 1:",result1)

allpackets = sorted(lines + [[[2]], [[6]]], key = cmp_to_key(compare))

print("Part 2:", (allpackets.index([[2]])+1)*(allpackets.index([[6]])+1))
