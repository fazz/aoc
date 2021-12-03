
text_file = open("input02.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

aim = 0
depth = 0
pos = 0

for l in lines:
    (c, n) = l.split(' ')
    n = int(n)

    if c == 'down':
        aim += n
    elif c == 'up':
        aim -= n
    else:
        pos += n
        depth += n*aim

print("Part1: ", aim*pos)
print("Part2: ", depth*pos)
