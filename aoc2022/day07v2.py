
lines = [x.rstrip("\n\r") for x in open("input07.txt", "r").readlines()]

stack = []
allsizes = []

for l in lines:
    c = l.split(' ')

    if c[0] == "$":
        if c[1] == "ls":
            pass
        elif c[2] == "..":
            cwd = stack.pop()
            stack[-1][1] += cwd[1]
            allsizes.append(cwd[1])
        else:
            stack.append([c[2], 0])
    else:
        if not c[0] == "dir":
            stack[-1][1] += int(c[0])

while len(stack) > 1:
    cwd = stack.pop()
    stack[-1][1] += cwd[1]

requiredspace = -40000000 + stack[0][1]

print("Part 1:", sum(filter(lambda x: x <= 100000, allsizes)))

print("Part 2:", min(filter(lambda x: x >= requiredspace, allsizes)))
