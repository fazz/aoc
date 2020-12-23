text_file = open("input22.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

x = lines.index('')
stack1 = [int(x) for x in lines[1:x]]
stack2 = [int(x) for x in lines[x+2:]]

# returns winner number
def play(stack1, stack2, part2):
    loopcheck = set()
    while len(stack1) > 0 and len(stack2) > 0:
        c1 = tuple(stack1)
        c2 = tuple(stack2)
        if (c1,c2) in loopcheck:
            return (1, [], [])
        loopcheck.add((c1, c2))

        a = stack1.pop(0)
        b = stack2.pop(0)

        if part2 and len(stack1) >= a and len(stack2) >= b:
            (r, s1, s2) = play(stack1[:a], stack2[:b], part2)
            if r == 1:
                stack1.append(a)
                stack1.append(b)
            else:
                stack2.append(b)
                stack2.append(a)
        else:
            if a > b:
                w = stack1
            else:
                w = stack2
            w.append(max(a,b))
            w.append(min(a,b))

    return (1 if len(stack1) > 0 else 2, stack1, stack2)

def calc(stack1, stack2, part2):
    (w, stack1, stack2) = play(stack1, stack2, part2)

    w = stack1 if len(stack1) > 0 else stack2

    return sum([w[i] * (len(w) - i) for i in range(len(w))])

print("Part1:", calc(stack1[:], stack2[:], False), 36257)
print("Part2:", calc(stack1, stack2, True), 33304)

