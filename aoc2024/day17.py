
import sys
sys.path.insert(0, "../aoc2023")

from operator import xor
from parse import parse
from aocd import data, post

input = data.split('\n')

a = parse("Register A: {:d}", input[0])[0]
b = parse("Register B: {:d}", input[1])[0]
c = parse("Register C: {:d}", input[2])[0]

program = tuple(map(int, tuple(input[4].split(' '))[1].split(',')))

def calc(a, b, c, output):

    pc = 0

    success = True

    def combo(v):
        if v >= 0 and v <= 3:
            return v
        elif v == 4:
            return a
        elif v == 5:
            return b
        elif v == 6:
            return c

    while pc < len(program) and success:
        i = program[pc]
        o = program[pc+1]
        npc = pc + 2
        if i == 0:
            # adv
            a = a // (2**combo(o))
        elif i == 1:
            # bxl
            b = xor(b, o)

        elif i == 2:
            # bst
            b = combo(o) % 8
        
        elif i == 3:
            # jnz
            if a != 0:
                npc = o
        elif i == 4:
            # bxc
            b = xor(b, c)
        
        elif i == 5:
            # out
            if not output(combo(o) % 8):
                success = False

        elif i == 6:
            # bdv
            b = a // (2**combo(o))

        elif i == 7:
            # cdv
            c = a // (2**combo(o))

        pc = npc

    return success

output1 = []

def out1(v):
    output1.append(v)
    return True

calc(a, b, c, out1)

r1 = ','.join(map(str, output1))
post.submit(r1, part="a", day=17)

output2 = []
ignored = len(program)-4

def out2(v):
    global output2
    global ignored
    i = len(output2)
    if v != program[ignored+i]:
        output2 = []
        return False
    output2.append(v)
    return True

bits = 12
rng = 2**bits
grw = 2**(bits-3)

print(program)

a = 0
r2 = 0
while ignored >= 0:
    for ad in range(0, rng):
        c = 0
        r = calc(a*rng+ad, 0, 0, out2)
        if r:
            if len(output2) == len(program)-ignored:# and output2 == program[ignored-1:]:
                a = a*8 + ad//grw
                r2 = a//8*rng+ad
                ignored = ignored - 1
                    
                break

post.submit(r2, part="b", day=17)
