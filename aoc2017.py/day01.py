
text_file = open("input01.txt", "r")

line = [x.rstrip("\n\r") for x in text_file.readlines()][0]

ll = len(line)

result1 = 0

for i in range(ll):
    if line[i] == line[(i+1)%ll]:
        result1 += int(line[i])

print("Part 1:", result1)

result2 = 0

for i in range(ll):
    if line[i] == line[(i+ll//2)%ll]:
        result2 += int(line[i])

print("Part 2:", result2)

