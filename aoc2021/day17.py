from collections import defaultdict
from math import isqrt
from datetime import datetime

tstart = datetime.now()

(x1, x2) = (79,137)
(y2, y1) = (-176,-117)

#(x1, x2) = (20,30)
#(y2, y1) = (-10,-5)

def asum(end, start):
    n = end - start + 1
    return (2*start+n-1)*n // 2

ysteps = defaultdict(list)

ms = isqrt(8*-y2)

for s in range(y2, 1):
    for step in range(ms):
        yy = -asum(-s+step, -s)
        if y2 <= yy <= y1:
            ysteps[step].append(s)
            ysteps[step - 2*(s+1) + 1].append(-s-1)

speeds = set()
cycles = 0
for xspeed in range(x2+1):
    for endstep in range(xspeed+1):
        d = xspeed - endstep
        s = asum(xspeed, d)
        if s > x2:
            break
        elif s >= x1:
            m = (-y2*2) if d == 0 else endstep+1
            for es in range(endstep, m):
                speeds.update([(xspeed, ys) for ys in ysteps[es]])

print("Part2:", len(speeds))
print("Part2 time:", (datetime.now() - tstart).microseconds // 1000, "ms")
