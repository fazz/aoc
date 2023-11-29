
from aocd import data, post
from functools import reduce
from collections import defaultdict
import operator
import re
import sys

input = data.split('\n')

def rreg(value, regs):
    if value[0] in ('-', '+'):
        f = value[1:].isdigit()
    else:
        f = value.isdigit()
    if f:
        return int(value)
    return regs[value]

r1 = 0

def calc(prg, context, part):
    global r1

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
    elif op == "sub":
        arg2 = rreg(arg2, reg)
        reg[arg1] -= arg2
    elif op == "mul":
        arg2 = rreg(arg2, reg)
        reg[arg1] *= arg2
        r1 += 1
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
    elif op == "jnz":
        arg1 = rreg(arg1, reg)
        arg2 = rreg(arg2, reg)
        if arg1 != 0:
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
    if terminated:
        break

post.submit(r1, part="a", day=23, year=2017)

############

primes = None

def is_prime(x):
    global primes
    if primes is None:
        primes = set()
        c = list(range(2, 130000))
        f = [False for x in range(2, 130000)]
        i = 0
        while i < len(c):
            while i < len(f) and f[i]:
                i += 1
            if i >= len(c):
                break
            p = c[i]
            i2 = i + p
            while i2 < len(c):
                f[i2] = True
                i2 += p
            i += 1
        primes = set([c[i-2] for i in range(2, 130000) if not f[i-2]])

    return x in primes

b = 84
b = b * 100 + 100000
c = b + 17000

h = 0

while b <= c:
    if not is_prime(b):
        h += 1
    b += 17

r2 = h

post.submit(r2, part="b", day=23, year=2017)
