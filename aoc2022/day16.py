import datetime
from copy import deepcopy
from itertools import compress
from functools import reduce, cmp_to_key
import operator
from collections import defaultdict
import re

from segments import intersect

from queue import PriorityQueue

start_time = datetime.datetime.now()

lines = [x.rstrip(" \n\r") for x in open("input16.txt", "r")]

flows = {}
tunnels = {}

for l in lines:
    g = re.search('Valve (.+) has flow rate=([0-9]+); tunnel([s])* lead([s])* to valve([s])* (.+)', l)

    valve = g.group(1)
    flow = int(g.group(2))
    tnls = [x.rstrip(',') for x in g.group(6).split(' ')]

    flows[valve] = flow
    tunnels[valve] = tnls

open = set()

for (v, f) in flows.items():
    if f == 0:
        open.add(v)

result1 = 0

Z = 30*sum(flows.values())

q = PriorityQueue()

dist = {i: Z+1 for i in flows.keys()}
dist['AA'] = Z

flowinverse = Z

for i in flows.keys():
    if i == 'AA':
        # dist, id, flow, steps, avatud
        q.put((Z, i, 0, 0, open))
    else:
        q.put((Z+1, i, 0, 0, open))

while q.qsize() > 0:
    #print("q:", q.queue)
    v = q.get()

    (d, id, flow, steps, open) = v

    if dist[id] < d:
        continue

    print(id, open)
    if id not in open:
        alt = Z - flow*(steps+1) - flows[id]
        print("alt on open:", id, alt)
        if alt < dist[id]:
            dist[id] = alt
            q.put( (dist[id], id, flow+flows[id], steps+1, open.union([id])) )

    for t in tunnels[id]:
        print("processing:", id, t, steps)
        alt = Z - flow*(steps+1)
        if alt < dist[t]:
            dist[t] = alt
            if steps+1 < 30:
                q.put((dist[t], t, flow, steps+1, open))


print(dist)

import sys
sys.exit(0)




result1 = 0

def maxpotentential(timeleft, flow, totalflown, values):
    maximum = totalflown + timeleft*flow
    c = sorted(values)
    for x in range(timeleft//2):
        if len(c) == 0:
            break
        v = c.pop()
        maximum += (timeleft-(x+1)*2+1)*v

    return maximum

def search(timeleft, open, next, prev, flow, totalflown):
    global result1

    result1 = max(result1, totalflown)

    c = [flows[x] for x in set(flows.keys()).difference(open)]

    maximum = maxpotentential(timeleft, flow, totalflown, c)

    if maximum <= result1:
        return

    if len(open) == len(flows):
        result1 = maximum
        return

    if timeleft == 0:
        return

    for o in (True, False) if next not in open else (False,): #Kas ma avan konkreetse kraani?
        if o:
            search(timeleft-1, open.union([next]), next, next, flow+flows[next], totalflown+flow)
        else:
            t = filter(lambda x: x != prev, sorted(tunnels[next], key=lambda x: flows[x] if x not in open else 0, reverse=True))

            for n in t:
                search(timeleft-1, open, n, next, flow, totalflown+flow)

search(30, open, "AA", "AA", 0, 0)
print("Part 1:", result1)

result2 = 0

def maxpotentential2(timeleft, flow, totalflown, values):
    maximum = totalflown + timeleft*flow
    c = sorted(values)
    for x in range(timeleft//2):
        if len(c) == 0:
            break
        v = c.pop()
        maximum += (timeleft-(x+1)*2+1)*v
        if len(c) == 0:
            break
        v = c.pop()
        maximum += (timeleft-(x+1)*2+1)*v

    return maximum

def search2(counter, state, timeleft, open, flow, addflow, totalflown, flowpath):
    global result2

    (next, prev) = state[counter]

    if result2 < totalflown:
        print("r2:", result2, totalflown)
    result2 = max(result2, totalflown)

    if result2 == 1933:
        print("got it")

    c = [flows[x] for x in set(flows.keys()).difference(open)]

    maximum = maxpotentential2(timeleft, flow, totalflown, c)

    if counter == 0:
        if maximum <= result2:
            return

        if len(open) == len(flows):
            result2 = maximum
            return

        if timeleft == 0:
            return

    ncounter = (counter + 1) % 2

    if ncounter == 0:
        td = 1
    else:
        td = 0

    nstate = deepcopy(state)

    for o in (True, False) if next not in open else (False,):
        if o:
            nstate[counter] = (next, next)
            if ncounter == 0:
                f = (flow+addflow+flows[next], 0)
            else:
                f = (flow, addflow+flows[next])
            search2(ncounter, nstate, timeleft-td, open.union([next]), *f, totalflown+flow*td, flowpath+[(timeleft, counter, flow+flows[next])])
        else:
            t = filter(lambda x: x not in [v for s in state for v in s], sorted(tunnels[next], key=lambda x: flows[x] if x not in open else 0, reverse=True))
            for n in t:
                nstate[counter] = (n, next)
                if ncounter == 0:
                    f = (flow+addflow, 0)
                else:
                    f = (flow, addflow)
                search2(ncounter, nstate, timeleft-td, open, *f, totalflown+flow*td, flowpath+[(timeleft, counter, flow)])


search2(0, [("AA", "AA"), ("AA", "AA")], 26, open, 0, 0, 0, [])
print("Part 2:", result2)

end = datetime.datetime.now()

print("Milliseconds:", (end-start_time).seconds*1000 + (end-start_time).microseconds // 1000)
