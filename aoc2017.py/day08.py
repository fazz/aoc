import re
from collections import defaultdict

text_file = open("input08.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

registers = defaultdict(lambda: 0)

maxv = 0

for l in lines:
    (register, op, diff, iff, cregister, comp, value) = l.split(' ')

    diff = int(diff)
    r = eval('registers[\'' + cregister + '\'] ' + comp + ' ' + value)
    d = -1 if op == 'dec' else 1

    if r:
        registers[register] = registers[register] + d*diff
        maxv = max(maxv, registers[register])

print("Part 1:", max(registers.values()))
print("Part 2:", maxv)
