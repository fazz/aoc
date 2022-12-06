text_file = open("input04.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

result1 = 0
result2 = 0

for l in lines:
    (a,b) = l.split(',')
    (b1,e1) = (tuple(map(int, a.split('-'))))
    (b2,e2) = (tuple(map(int, b.split('-'))))

    if (b1 >= b2 and e1 <= e2) or (b2 >= b1 and e2 <= e1):
        result1 += 1
    
    s1 = set(range(b1, e1+1))
    s2 = set(range(b2, e2+1))

    if len(s1.intersection(s2)) > 0:
        result2 += 1

print("Part 1:", result1)
print("Part 2:", result2)
