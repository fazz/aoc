import re

text_file = open("input07.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

lhs = set()
rhs = set()

rules = {}

for l in lines:
    
    e = re.split(' -> |, | ', l)

    lhs.add(e[0])
    rhs.update(e[2:])

    rules[e[0]] = [int(e[1][1:-1])] + e[2:]

start = lhs.difference(rhs).pop()

print("Part 1:", start)


def verify(term):

    if len(rules[term] > 1):
        ws = []
        for d in rules[term][1:]:
            (w, b) = verify(d)
            if b:
                return (w,b)
            ws.append(verify(d))

    return 0