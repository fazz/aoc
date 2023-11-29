
text_file = open("input09.txt", "r")

line = [x.rstrip("\n\r") for x in text_file.readlines()][0]

normal = True

ll = len(line)

i = 0
level = 1

result1 = 0
result2 = 0

while i < ll:
    if normal:
        if line[i] == '{':
            result1 += level
            level += 1
        elif line[i] == '}':
            level -= 1
        elif line[i] == '<':
            normal = False
        i += 1
    else:
        if line[i] == '!':
            i += 1
        elif line[i] == '>':
            normal = True
        else:
            result2 += 1
        i += 1

print("Part 1:", result1)
print("Part 2:", result2)