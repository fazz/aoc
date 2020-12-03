text_file = open("input03.txt", "r")
lines = text_file.readlines()

rows = []
rowlen = 0

for l in lines:
    l = l.strip()
    rows.append(l)

rowlen = len(rows[0])
rowcount = len(rows)

def count(dx, dy):
    (x, y) = (0, 0)
    res = 0
    
    while y < rowcount-1:
        x = (x + dx) % rowlen
        y = y + dy
        res += 1 if rows[y][x] == '#' else 0
    return res

print("Part1:", count(3, 1))
print("Part2:", count(1, 1) * count(3, 1) * count(5, 1) * count(7, 1) * count(1, 2))
