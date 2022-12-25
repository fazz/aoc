
from collections import defaultdict
import re
from heapq import *

lines = [x.rstrip(" \n\r") for x in open("input19.txt", "r")]
inputbp = {}

for l in lines:
    g = re.search(' ([0-9]+):.+ ([0-9]+) .+ ([0-9]+) .+ ([0-9]+) .+ ([0-9]+) .+ ([0-9]+) .+ ([0-9]+) obsidian', l)

    inputbp[int(g.group(1))] = (int(g.group(2)), int(g.group(3)), int(g.group(4)), int(g.group(5)), int(g.group(6)), int(g.group(7)))

def find(bp, minutes):
    (orecost, claycost, obscost1, obscost2, crackcost1, crackcost2) = bp

    state = (1, 0, 0, 0, 0, 0, 0)
    
    dist = defaultdict(lambda: 2**32-1)

    dist[(0, state)] = 0
    visited = set([state])

    q = []
    heappush(q, (0, (0, state)))
  
    while len(q) > 0:
        u = heappop(q)
        (dd, vv) = u
        
        (minute, (orerobots, clayrobots, obsidianrobots, ore, clay, obsidian, crackers)) = vv

        if minute == minutes:
            return (1+minutes)*minutes//2-dd

        potential = []

        obsbotrequired = crackcost2*orerobots//crackcost1 - obsidianrobots

        claybotsrequired = obscost2*orerobots//obscost1 - clayrobots

        orebotsrequired1 = obscost1*clayrobots//obscost2 - orerobots
        orebotsrequired2 = crackcost1*obsidianrobots//crackcost2 - orerobots

        orebotsrequired3 = claycost - orerobots

        orebotsrequired = max(orebotsrequired1, orebotsrequired2, orebotsrequired3)

        if ore >= crackcost1 and obsidian >= crackcost2:
            potential.append((minute+1, (orerobots, clayrobots, obsidianrobots, ore+orerobots-crackcost1, clay+clayrobots, obsidian+obsidianrobots-crackcost2, crackers+1)))
        else:
            if ore >= obscost1 and clay >= obscost2 and obsbotrequired > 0:
                potential.append((minute+1, (orerobots, clayrobots, obsidianrobots+1, ore+orerobots-obscost1, clay+clayrobots-obscost2, obsidian+obsidianrobots, crackers)))
            else:
                if ore >= claycost and claybotsrequired > 0:
                    potential.append((minute+1, (orerobots, clayrobots+1, obsidianrobots, ore+orerobots-claycost, clay+clayrobots, obsidian+obsidianrobots, crackers)))

                if ore >= orecost and orebotsrequired > 0:
                        potential.append((minute+1, (orerobots+1, clayrobots, obsidianrobots, ore+orerobots-orecost, clay+clayrobots, obsidian+obsidianrobots, crackers)))

            potential.append((minute+1, (orerobots, clayrobots, obsidianrobots, ore+orerobots, clay+clayrobots, obsidian+obsidianrobots, crackers)))

        realdist = dist[vv]

        for v in potential:
            (nextminute, state) = v
            (orerobots, clayrobots, obsidianrobots, ore, clay, obsidian, _) = state

            alt = realdist + nextminute - crackers

            if state not in visited:
                visited.add(state)

                if alt < dist[v]:
                    dist[v] = alt

                    heappush(q, (dist[v], v))
    return None

result1 = 0

for (bpi, bpv) in inputbp.items():
    r = find(bpv, 24)

    if r == None:
        continue

    result1 += r*bpi

print("Part 1:", result1)

result2 = 1

for (bpi, bpv) in tuple(inputbp.items())[0:3]:
    r = find(bpv, 32)
    result2 *= r

print("Part 2:", result2)
