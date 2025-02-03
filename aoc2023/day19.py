
from aocd import data, post
from functools import reduce
from collections import defaultdict
from parse import parse
from operator import lt, gt

from aoc import factor

input = data.split('\n')

gapi = input.index("")

wfs = {}

for li in range(gapi):
    (n, inst) = parse('{}{{{}}}', input[li])
    wfs[n] = inst

def parsewf(wf):
    s = wf.split(',')

    r = []

    for step in s:
        if ':' not in step:
            r.append((step,))
        else:
            (eq, d) = step.split(':')
            if '<' in eq:
                r.append((eq[0], lt, int(eq[2:]), d))
            elif '>' in eq:
                r.append((eq[0], gt, int(eq[2:]), d))
    return r

def calca(e):
    c = 'in'
    dec = None
    while dec is None:
        inst = wfs[c]

        wf = parsewf(inst)

        for step in wf:
            if len(step) == 1:
                dec = step[0]
            else:
                if step[1](e[step[0]], step[2]):
                    dec = step[3]
            if dec is not None:
                break

        if dec not in ('A', 'R'):
            c = dec
            dec = None
    return dec

r1 = 0

for li in range(gapi+1, len(input)):

    v = list(parse('{{{}={},{}={},{}={},{}={}}}', input[li]))
    e = {x[0]:int(x[1]) for x in [(v[2*i], v[2*i+1]) for i in range(len(v)//2)]}

    dec = calca(e)
    
    if dec == 'A':
        r1 += sum(e.values())

print("r1:", r1)

post.submit(r1, part="a", day=19)

decisions = [['in']]

while True:
    for i in range(len(decisions)):

        if decisions[i][-1] in ('A', 'R'):
            continue

        c = decisions[i].pop()
        dec = None
        while dec is None:
            inst = wfs[c]

            wf = parsewf(inst)

            for step in wf:
                if len(step) == 1:
                    dec = step[0]
                else:
                    z = step[:3]

                    decisions.append(decisions[i] + [z, step[3]])

                    if step[1] == lt:
                        z = (step[0], gt, step[2]-1)
                    else:
                        z = (step[0], lt, step[2]+1)
                    decisions[i].append(z)

        c = decisions[i].append(dec)
    if len([x[:-1] for x in decisions if x[-1] in ('A', 'R')]) == len(decisions):
        break

decisions = [x[:-1] for x in decisions if x[-1] == 'A']

r2 = 0

for d in decisions:
    l = defaultdict(lambda: 1)
    u = defaultdict(lambda: 4000)

    for e in d:
        if e[1] == lt:
            u[e[0]] = e[2]-1
        if e[1] == gt:
            l[e[0]] = e[2]+1

    [(l[k], u[k]) for k in ('x', 'm', 'a', 's')]

    r2 += reduce(lambda o, v: o*(u[v]-l[v]+1), l.keys(), 1)

print("r2:", r2)

post.submit(r2, part="b", day=19)
