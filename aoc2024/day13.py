
import sys
sys.path.insert(0, "../aoc2023")

from parse import parse

from aocd import data, post

import sympy as sp
from sympy.solvers import solve

input = data.split('\n')

(a, b, cost) = sp.symbols('a, b, cost', positive=True, integer=True)

r1 = 0
r2 = 0
for x in range((len(input)+1)//4):
    eqs = list()

    ap = parse("Button A: X+{:d}, Y+{:d}", input[x*4])
    bp = parse("Button B: X+{:d}, Y+{:d}", input[x*4+1])
    pr = parse("Prize: X={:d}, Y={:d}", input[x*4+2])

    eqs.append(sp.Eq(pr[0], a*ap[0]+b*bp[0]))
    eqs.append(sp.Eq(pr[1], a*ap[1]+b*bp[1]))

    output = solve(eqs, dict=True)

    if len(output):
        r1 += output[0][a]*3+output[0][b]

    eqs = list()

    eqs.append(sp.Eq(pr[0]+10000000000000, a*ap[0]+b*bp[0]))
    eqs.append(sp.Eq(pr[1]+10000000000000, a*ap[1]+b*bp[1]))

    output = solve(eqs, dict=True)

    if len(output):
        r2 += output[0][a]*3+output[0][b]

r1 = int(r1)
r2 = int(r2)

post.submit(r1, part="a", day=13)
post.submit(r2, part="b", day=13)
