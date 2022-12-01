
text_file = open("input01.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

cals = []
cal = 0

i = 0
while "" in lines[i:]:
    nxt = i + lines[i:].index("")
    cals.append([int(x) for x in lines[i:nxt]])
    i = nxt + 1
cals.append([int(x) for x in lines[i:]])
cals = sorted([sum(x) for x in cals], reverse=True)

print("Part 1:", cals[0])

print("Part 2:", sum(cals[0:3]))