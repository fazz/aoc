
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter
from itertools import chain, pairwise, accumulate
from copy import deepcopy
import operator
import re
import sys
import networkx as nx


from aoc import factor

input = data.split('\n')

xinput = [
'broadcaster -> a',
'%a -> inv, con',
'&inv -> b',
'%b -> con',
'&con -> rx',
]

xinput = [
'broadcaster -> a, lf, rz, fk',
'%a -> br, b',
'%b -> c',
'%c -> br',
'&br -> c, a, lb',
'&lf -> lb',
'&rz -> lb',
'&fk -> lb',
'&lb -> rx',
]

origmods = {}
sources = defaultdict(list)

for l in input:
    (source, t) = l.split(' -> ')
    targets = t.split(', ')

    if source == "broadcaster":
        origmods[source] = (1, targets)
        sk = source
    elif source[0] == '%':
        origmods[source[1:]] = (2, targets, [0])
        sk = source[1:]
    elif source[0] == '&':
        origmods[source[1:]] = (3, targets, [], {})
        sk = source[1:]
    for t in targets:
        sources[t].append(sk)

for e in origmods.items():
    for t in e[1][1]:
        if t not in origmods:
            continue
        if origmods[t][0] == 3:
            origmods[t][2].append(e[0])
            origmods[t][3][e[0]] = 0

def simulate(mods, sendingnode = None, collected = None, sendinglevel = 0):
    sent = defaultdict(int)
    triggered = []
    monitor = defaultdict(lambda: {'sent': defaultdict(int), 'state': None})

    q = []

    q.append((None, 'broadcaster', 0))

    while len(q) > 0:
        (src, target, signallevel) = q.pop(0)

        sent[signallevel] += 1
        if target not in mods:
            continue

        moddata = mods[target]
        targets = mods[target][1]

        #if target == "lf":
        #    print(moddata)

        sendlevel = None

        if moddata[0] == 1:
            sendlevel = 0
        elif moddata[0] == 2:
            if signallevel == 0:
                moddata[2][0] = 0 if moddata[2][0] == 1 else 1
                sendlevel = moddata[2][0]
                if collected is not None and target in collected:
                    monitor[target]['state'] = moddata[2][0]
                    monitor[target]['sent'][sendlevel] += 1

        elif moddata[0] == 3:
            inputs = moddata[3]
            inputs[src] = signallevel
            sendlevel = 0 if sum(inputs.values()) == len(inputs) else 1

        if sendlevel is not None:
            for t in targets:
                q.append((target, t, sendlevel))
            if sendingnode is not None and target in sendingnode:
                if sendlevel == sendinglevel:
                    triggered.append(target)

    return (mods, sent, triggered, monitor)

# p1

mods = deepcopy(origmods)

r1 = 0
r1l = 0
r1h = 0
for _ in range(1000):
    (mods, sent, _, _) = simulate(mods)
    r1l += sent[0]
    r1h += sent[1]

r1 = r1h*r1l
print("r1:", r1, sent)

post.submit(r1, part="a", day=20)

# p2

G = nx.DiGraph()

for (s,t) in origmods.items():
    G.add_node(s)
    for target in t[1]:
        G.add_node(target)
        G.add_edge(s, target)

c = nx.attracting_components(G)
print(c)
for cc in c:
    print(cc)


r2 = 1

monitored = ["nn", "zc", "ms", "tp", "hf", "qk", "zb", "gz", "vf", "nc", "sf", "xv"]
monitor = defaultdict(lambda: {'sent': defaultdict(int), 'state': None})

interesting = ["br", "lf", "fk", "rz"]
#interesting = []
counts = {}
mods = deepcopy(origmods)

i = 1
while True:
    (mods, _, results, collected) = simulate(mods, interesting, monitored, 1)
    for r in results:
        if r not in counts:
            counts[r] = i
    print("Round:", i)
    for m in monitored:
        for k in collected[m]['sent'].keys():
            monitor[m]['sent'][k] += collected[m]['sent'][k]
        if collected[m]['state'] is not None:
            monitor[m]['state'] = collected[m]['state']
        print(monitor[m]['state'], dict(monitor[m]['sent']))
    if len(counts) == len(interesting):
        break
    i += 1

r2 = list(accumulate(counts.values(), lambda a, b: a*b, initial = 1))[-1]

print("r2:", r2, counts)

post.submit(r2, part="b", day=20)


#sys.exit(0)

r2 = 250924073918341

print("r2:", r2)

post.submit(r2, part="b", day=20)


labels = {"rx":"rx"}
for (k,v) in origmods.items():
    if v[0] == 1:
        labels[k] = k
    elif v[0] == 2:
        labels[k] = "F" + k
    elif v[0] == 3:
        labels[k] = "C" + k


with open('day20.dot', 'w') as out:

    print("digraph G {", file=out)
    for (k,v) in origmods.items():

        if v[0] == 1:
            print(labels[k] + " -> {" + ' '.join(map(lambda x: labels[x], v[1])) + "};", file=out)
        elif v[0] == 2:
            print(labels[k] + " -> {" + ' '.join(map(lambda x: labels[x], v[1])) + "};", file=out)
        elif v[0] == 3:
            print(labels[k] + " -> {" + ' '.join(map(lambda x: labels[x], v[1])) + "};", file=out)

    print("}", file=out)