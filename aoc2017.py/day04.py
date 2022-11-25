text_file = open("input04.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

result1 = 0

for l in lines:
    s = l.split(' ')
    result1 += 1 if len(s) == len(set(s)) else 0

print("Part 1:", result1)

result2 = 0

for l in lines:
    s = [''.join(sorted(x)) for x in l.split(' ')]
    result2 += 1 if len(s) == len(set(s)) else 0

print("Part 2:", result2)