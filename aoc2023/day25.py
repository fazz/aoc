
from aocd import data, post
from functools import reduce, cmp_to_key
from collections import defaultdict, Counter
from itertools import chain
import operator
import re
import sys
import networkx as nx

from aoc import factor, all_pairwise_undirected

input = data.split('\n')

G = nx.DiGraph()

nodes = []

for l in input:
    (s, t) = l.split(': ')
    ts = t.split()

    G.add_node(s)
    nodes.append(s)

    nodes.extend(ts)
    for t in ts:
        G.add_node(t)
        G.add_edge(s, t, capacity=1)

G = G.to_undirected(reciprocal=False)

for (a, b) in all_pairwise_undirected(nodes):
    r = nx.minimum_cut(G, a, b)
    if r[0] == 3:
        break

r1 = reduce(operator.mul, map(len, r[1]), 1)

print("r1:", r1)

post.submit(r1, part="a", day=25)
