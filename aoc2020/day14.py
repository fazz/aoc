
text_file = open("input14.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def calc(part1):
    andmasks = []
    ormasks = []
    memory = {}
    for l in lines:
        (pref, suf) = l.split('=')
        pref = pref.rstrip()
        if pref == 'mask':
            andmasks = [0]
            ormasks = [0]
            for c in suf:
                for mi in range(len(andmasks)):
                    andmasks[mi] *= 2
                    ormasks[mi] *= 2
                    if c == 'X':
                        a = andmasks[mi]
                        andmasks[mi] = a | 1

                        o = ormasks[mi]
                        ormasks[mi] = o | (0 if part1 else 1)

                        if not part1:
                            andmasks.append(a | 0)
                            ormasks.append(o | 0)
                    elif c == '0':
                        if part1:
                            andmasks[mi] = andmasks[mi] | 0
                            ormasks[mi] = ormasks[mi] | 1
                        else:
                            andmasks[mi] = andmasks[mi] | 1
                            ormasks[mi] = ormasks[mi] | 0
                    elif c == '1':
                        andmasks[mi] = andmasks[mi] | 1
                        ormasks[mi] = ormasks[mi] | 1
        else:
            value = int(suf)
            pos = int(pref[4:-1])

            if part1:
                memory[pos] = (value | ormasks[0]) & andmasks[0]
            else:
                for mi in range(len(andmasks)):
                    memory[(pos | ormasks[mi]) & andmasks[mi]] = value

    return sum(memory.values())

print("Part1:", calc(True))
print("Part2:", calc(False))
