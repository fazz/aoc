
text_file = open("input08.txt", "r")

program = [(lambda a: (a[0], int(a[1])))(x.rstrip("\n\r").split(' ')) for x in text_file.readlines()]

def exec(program):
    acc = 0
    pc = 0
    run = set()
    code = -1

    while True:
        if pc in run:
            code = 0
            break
        if pc == len(program):
            code = 1
            break
        if pc < 0 or pc > len(program):
            code = 2
            break
        c = program[pc]
        if c[0] == "nop":
            run.add(pc)
            pc += 1
            continue
        elif c[0] == "jmp":
            run.add(pc)
            pc += c[1]
            continue
        elif c[0] == "acc":
            run.add(pc)
            acc += c[1]
            pc += 1
            continue
    return (acc, code, run)

(acc, r, part1trace) = exec(program)

print("Part1:", acc)

def flip(program, i):
    if program[i][0] == "jmp":
        program[i] = ("nop", program[i][1])
    elif program[i][0] == "nop":
        program[i] = ("jmp", program[i][1])
    else:
        return (program, False)
    return (program, True)

part2 = 0
for i in part1trace:
    (program, f) = flip(program, i)
    if not f:
        continue
    (part2, r, trace) = exec(program)
    (program, f) = flip(program, i)
    if r == 1:
        break

print("Part2:", part2)

#
#
#
plen = len(program)
chart = {}
def changeinst(idx):
    global plen, program
    (i, os) = program[idx]
    o = idx + os
    alto = idx + 1
    if i == "nop":
        o, alto = alto, o
    elif i == "acc":
        o = alto
    if 0 <= o <= plen:
        chart.setdefault(o, []).append(idx)
    return alto

alto = [changeinst(x) for x in range(plen)]

# fold 
queue = set(chart[plen])
reachable = set([plen])
while len(queue) > 0:
    e = queue.pop()
    queue = queue.union(chart.setdefault(e, set()))
    reachable = reachable.union(chart.setdefault(e, set()))

idx = list(filter(lambda x: alto[x] in reachable, part1trace))[0]

(program, f) = flip(program, idx)
(part2, r, trace) = exec(program)
print("Part2:", part2)
