
import sys
sys.path.insert(0, "../aoc2023")

from aocd import data, post
from itertools import product, combinations
from operator import and_, or_, xor
from parse import parse
from collections import deque

from aoc import transposestringmatrix, filtersplit


xdata="""x00: 1
y00: 1
x01: 0
y01: 0

x00 XOR y00 -> z00
x00 AND y00 -> carry_00
x01 XOR y01 -> sum_01
x01 AND y01 -> carry_01
sum_01 XOR carry_00 -> z02
sum_01 AND carry_00 -> halfcarry_01
carry_01 OR halfcarry_01 -> z01"""


xdata="""x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""

input = list(map(lambda x: x.split('\n'), data.split('\n\n')))

op = {'AND': and_, 'OR': or_, 'XOR': xor }
nums = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

x = 0
y = 0
iwires = {y[0]: int(y[1]) for y in [x.split(': ') for x in input[0]]}
for (k, v) in iwires.items():
    p = k[0]
    a = 2**int(k[1:])*v
    if p == 'x':
        x += a
    else:
        y += a

wirelist = set()

ocount = 0
rules = []
types = {}

for expr in input[1]:
    ap = parse("{op1:w} {op:w} {op2:w} -> {res:w}", expr)
    rules.append([ap['op1'], ap['op'], ap['op2'], ap['res']])
    wirelist.add(ap['res'])

    if ap['res'][0] == 'z' and ap['res'][1] in nums and ap['res'][2] in nums:
        ocount = max(ocount, int(ap['res'][1:]) + 1)
        rules.append((ap['res'], 'OUT', None, int(ap['res'][1:])))

########

changes = [
#    ('z07', 'nqk'),
#    ('pcp', 'fgt'),
#    ('fpq', 'z24'),
#    ('srn', 'z32')
    ]

def change(change):
    a = list(filter(lambda x: x[3] == change[0], rules))[0]
    b = list(filter(lambda x: x[3] == change[1], rules))[0]
    rules.remove(a)
    rules.remove(b)
    rules.append(a[:3] + [b[3]])
    rules.append(b[:3] + [a[3]])

for c in changes:
    change(c)


########

with open('day24.dot', 'w') as out:

    print("digraph G {", file=out)

    for e in rules:
        if e[2] is not None:
            opnode = e[1] + e[0] + e[2]
        else:
            opnode = e[1] + e[0]

        print(opnode + "[label = \"" + e[1] + "\"]", file=out)

        print(e[0] + " -> {" + opnode + "};", file=out)
        if e[2] is not None:
            print(e[2] + " -> {" + opnode + "};", file=out)
            print(opnode + " -> {" + e[3] + "};", file=out)

    print("}", file=out)

from math import log2

def compute(x, y):

    wires = {}

    s = ocount
    for i in range(s + 1):
        wires["x{:02d}".format(i)] = x & 1
        wires["y{:02d}".format(i)] = y & 1
        x >>= 1
        y >>= 1

    waitlist = deque(rules)

    empty = 0
    while len(waitlist):
        rule = waitlist.pop()
        if rule[0] not in wires or rule[2] not in wires:
            waitlist.appendleft(rule)
            empty += 1
            if empty >= len(waitlist):
                return 9999999999999999
        else:
            res = op[rule[1]](wires[rule[0]], wires[rule[2]])
            wires[rule[3]] = res
            empty = 0

    zs = filter(lambda x: x[0] == 'z', wires.keys())

    r1 = 0

    for z in zs:
        p = int(z[1:])
        r1 += 2**p*wires[z]

    return r1

r1 = compute(x, y)

print(r1)

post.submit(r1, part="a", day=24)


def biterrors():
    res = 0
    for i in range(45):
#        print("Bit: {:2d}".format(i))
        a = 2**i
        b = 2**i
#        v1 = compute(a, 0)
        v = compute(a, b)
        diff = (a+b) ^ v
        bit = 0
        while diff > 0:
            res += diff & 1
            if diff & 1 > 0:
                #print("broken bit:", bit)
                pass
            diff >>= 1
            bit += 1

#        print(v, a + b, v == a + b)
#        print(v1, a, v1 == a)
    return res

be = biterrors()

print("biterrors:", biterrors())


#for c in combinations(wirelist, 2):
#    #print(c)
#    change(c)
#    nbe = biterrors()
#    if nbe < be:
#        be = nbe
#        print(c)
#    else:
#        change(c)
#

#r2s = ["z07", "nqk", "pcp", "fgt", "fpq", "z24", "srn", "z32"]
#
#r2s = sorted(r2s)
#
#print(r2s)
#
#r2 = ",".join(r2s)
#
#print(r2)
#
#post.submit(r2, part="b", day=24)





waitlist = deque(rules)

broken = []
unclearinputs = {}

while len(waitlist):
    rule = waitlist.pop()

    #print("rule:", rule)
    #print(len(waitlist))

    #print("types :", types)

    (op1, op, op2, result) = rule
    if op == 'OUT':
        print(rule)

    if op1[0] in ('x', 'y') and op1[1] in nums and op1[2] in nums:
        types[op1] = ('input', int(op1[1:]))
        types[op2] = ('input', int(op2[1:]))

#        if op == 'AND':
#            types[result] = ('carry', int(op1[1:]))
#        elif op == 'OR':
#            types[result] = ('or', int(op1[1:]))
#        elif op == 'XOR':
#            types[result] = ('sum', int(op1[1:]))

    else:
        if not (op1 in types and op2 in types):
            waitlist.appendleft(rule)
            continue

    type1 = types[op1][0]
    rank1 = types[op1][1]

    if op2 is not None:
        type2 = types[op2][0]
        rank2 = types[op2][1]

    diff = rank1 - rank2
    if (type1 == 'output' and op == 'OUT'):
        # siia tuua z-nodede kontroll
        pass
    elif (type1 == 'input' and type2 == 'input'):
        if op == 'AND':
            if rank1 == 0:
                types[result] = ('carry', rank1)
            else:
                types[result] = ('mul', rank1)
        elif op == 'OR':
            types[result] = ('or', rank1)
        elif op == 'XOR':
            types[result] = ('sum', rank1)
        
    elif (((type1 == 'sum' and type2 == 'carry' and diff == 1) or
        (type1 == 'carry' and type2 == 'sum' and diff == -1))
        and (op == 'AND')):
        types[result] = ('halfcarry', max(rank1, rank2))
        pass

    elif (((type1 == 'sum' and type2 == 'carry' and diff == 1) or
        (type1 == 'carry' and type2 == 'sum' and diff == -1))
        and (op == 'XOR')):
        types[result] = ('output', max(rank1, rank2))
        pass

    elif (((type1 == 'halfcarry' and type2 == 'mul') or
        (type1 == 'mul' and type2 == 'halfcarry'))
        and (diff == 0) and op == 'OR'):
        types[result] = ('carry', rank1)

    else:
        print(types[op1], types[op2], ocount, broken, unclearinputs)

        unclearinputs[types[op1]] = op1
        unclearinputs[types[op2]] = op2

        if op == 'AND':
            if type1 == 'carry' or type2 == 'carry':
                t = 'sum'
                r = rank1 if type1 == 'carry' else rank2
                r += 1
            else:
                t = 'carry'
                r = rank1 if type1 == 'sum' else rank2
                r -= 1

            if (t, r) in unclearinputs:
                print((t, r), "found in unclearinputs")

            pass
        elif op == 'XOR':
            pass
        elif op == 'OR':
            pass
        elif op == 'OUT':
            print("OUT", rule)
            t = 'output'
            r = rule[3]
            if (t, r) in unclearinputs:
                print((t, r), "found in unclearinputs")
                broken.append[unclearinputs[(t, r)]]

        else:
            waitlist.appendleft(rule)

        #if op1 in broken:
        #    print(types[op1], "broken")
        #if op2 in broken:
        #    print(types[op2], "broken")
        #raise(rule)
    
    # Kas tuleks tüüp kodeerida operatsiooni juurde?
    # 
    
    # Vahepealne on katki kui:
    # 1) leidub mingi tema järglane, mis ei lahendu
    # 2) leidub mingi teine katkine, mis vastab järglase nõuetele

    # Kui ei 
    # Kui ei lahendu, topi eellased listi koos tüüpidega
    # 
    


    # Väljundite katkisuse tuvastamine
    # Saab generaliseerida, kodeerides z-noded operatioonidena?
    #if result == 'z00':
    #    if not types[result] == ('sum', 0):
    #        broken.append(result)
    #elif result[0] == 'z' and result[1] in nums and result[2] in nums and (int(result[1:])) < ocount - 1:
    #    if not types[result] == ('output', int(result[1:])):
    #        broken.append(result)
    #elif result == 'z{:02d}'.format(ocount-1):
    #    if not types[result] == ('highest', ocount-1):
    #        broken.append(result)
    #else:
    #    pass


print("broken:", broken)


