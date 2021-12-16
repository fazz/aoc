
from datetime import datetime
from enum import Enum
from itertools import accumulate

t1 = datetime.now()

text_file = open("input16.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

bits = ''.join(map(lambda x: "{0:0>4b}".format(int(x, 16)), lines[0]))

pc = 0

class S(Enum):
    START = 0,
    VER = 1,
    INTS = 2,
    LITERAL = 3,
    POP = 4,

s = S.START

part1 = 0
part2 = 0

stack = []

lengthbits = 0
lengthpackets = 0

while True:
    if s == S.POP:
        if len(stack):
            (type, packetstart, ti, lengthbits, lengthpackets, packetcount, subpackets) = stack.pop()
            subpackets.append(packetvalue)
            packetcount += 1
            if (ti == 1 and lengthpackets == packetcount) or (ti == 0 and packetstart + lengthbits <= pc) or (type == 4 and packetvalue[0] == 0):
                s = S.POP

                if type == 0:
                    packetvalue = sum(subpackets)
                elif type == 1:
                    packetvalue = tuple(accumulate(subpackets, lambda x,y: x*y, initial=1))[-1]
                elif type == 2:
                    packetvalue = min(subpackets)
                elif type == 3:
                    packetvalue = max(subpackets)
                elif type == 4:
                    packetvalue = tuple(accumulate(subpackets, lambda x,y: (x << 4) + y[1], initial=0))[-1]
                elif type == 5:
                    packetvalue = 1 if subpackets[0] > subpackets[1] else 0
                elif type == 6:
                    packetvalue = 1 if subpackets[0] < subpackets[1] else 0
                elif type == 7:
                    packetvalue = 1 if subpackets[0] == subpackets[1] else 0

                part2 = packetvalue
            else:
                s = S.LITERAL if type == 4 else S.START
                stack.append((type, packetstart, ti, lengthbits, lengthpackets, packetcount, subpackets))
        else:
            pc = ((pc // 8) + 1) * 8
            s = S.START
    elif s == S.START:
        if pc >= len(bits):
            break
        ver = int(bits[pc:pc+3], 2)
        part1 += ver
        pc += 3
        s = S.VER
    elif s == S.VER:
        type = int(bits[pc:pc+3], 2)
        pc += 3
        packetcount = 0
        if type == 4:
            s = S.LITERAL
            ti = 2
        else:
            ti = int(bits[pc])
            pc += 1
            if ti == 0:
                lengthbits = int(bits[pc:pc+15], 2)
                pc += 15
            else:
                lengthpackets = int(bits[pc:pc+11], 2)
                pc += 11
            s = S.START
        stack.append((type, pc, ti, lengthbits, lengthpackets, packetcount, []))

    elif s == S.LITERAL:
        flag = int(bits[pc], 2)
        value = int(bits[pc+1:pc+5], 2)
        packetvalue = (flag, value)
        pc += 5
        s = S.POP

print("Part1:", part1)
print("Part2:", part2)
