
start = [6,19,0,5,7,13,1]

def calc(count):
    sa = {}
    sb = { start[i] : i+1 for i in range(len(start))}

    turn = len(start)
    lastnumber = start[-1]

    while turn < count:
        sa[lastnumber] = sb.setdefault(lastnumber, turn)
        sb[lastnumber] = turn
        lastnumber = sb[lastnumber] - sa[lastnumber]
        turn += 1
    return lastnumber

print("Part1:", calc(2020))
print("Part2:", calc(30000000))

def calc2(count):
    h = { start[i] : i+1 for i in range(len(start))}

    l = 0

    for t in range(len(start)+1, count):
        p = h.setdefault(l, t)
        h[l] = t
        l = t - p

    return l

print("Part2:", calc2(30000000))
