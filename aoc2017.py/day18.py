
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re

input = data.split('\n')

def rreg(value, regs):
    if value[0] in ('-', '+'):
        f = value[1:].isdigit()
    else:
        f = value.isdigit()
    if f:
        return int(value)
    return regs[value]

def calc(prg, context, part):

    (pc, reg, sendq, recvq) = context

    sent = 0
    blocked = False
    terminated = False

    inst = prg[pc]
    dpc = 1

    p = inst.split(' ')
    if len(p) == 2:
        (op, arg1) = p
    else:
        (op, arg1, arg2) = p
    if op == "snd":
        arg1 = rreg(arg1, reg)
        sendq.append(arg1)
        sent += 1
    elif op == "set":
        arg2 = rreg(arg2, reg)
        reg[arg1] = arg2
    elif op == "add":
        arg2 = rreg(arg2, reg)
        reg[arg1] += arg2
    elif op == "mul":
        arg2 = rreg(arg2, reg)
        reg[arg1] *= arg2
    elif op == "mod":
        arg2 = rreg(arg2, reg)
        reg[arg1] %= arg2
    elif op == "rcv":
        if part == 1:
            arg1 = rreg(arg1, reg)
            if arg1 > 0:
                recv1.pop(0)
        else:
            if len(recvq) > 0:
                reg[arg1] = recvq.pop(0)
            else:
                blocked = True
                dpc = 0
    elif op == "jgz":
        arg1 = rreg(arg1, reg)
        arg2 = rreg(arg2, reg)
        if arg1 > 0:
            dpc = arg2
    pc += dpc

    if pc < 0 or pc >= len(prg):
        terminated = True

    return ((pc, reg, sendq, recvq), int(sent), blocked, terminated)

q = []
qlen = 0
context = (0, defaultdict(int), q, q)
while True:
    (context, sent, blocked, terminated) = calc(input, context, 2)
    if len(q) < qlen:
        break
    qlen = len(q)

r1 = q[-1]

post.submit(r1, part="a", day=18, year=2017)

recv0 = []
recv1 = []
contexts = [
    [(0, defaultdict(int, {'p': 0}), recv1, recv0), 0, False, False],
    [(0, defaultdict(int, {'p': 1}), recv0, recv1), 0, False, False]
]

p = 0
while not ((contexts[0][2] and contexts[1][2]) or (contexts[0][3] and contexts[1][3])):
    if not contexts[p][3]:
        (context, sent, blocked, terminated) = calc(input, contexts[p][0], 2)
        contexts[p][0] = context
        contexts[p][1] += sent
        contexts[p][2] = blocked
        if blocked and contexts[(p+1)%2][3]:
            terminated = True
        contexts[p][3] = terminated
    p = (p + 1) % 2

r2 = contexts[1][1]

post.submit(r2, part="b", day=18, year=2017)

