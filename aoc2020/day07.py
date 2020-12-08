import re

text_file = open("input07.txt", "r")
lines = text_file.readlines()

def maps(lines):
    result = {}
    result2 = {}

    for l in lines:
        sl = l.rstrip("\n\r").split(' ')
        outerb = sl[0] + " " + sl[1]
        if sl[4] != "no":
            for x in range((len(sl) - 4)//4):
                col = sl[5+(x*4)]+" "+sl[6+(x*4)]

                result.setdefault(col, set()).add(outerb)
                result2.setdefault(outerb, {})[col] = int(sl[4+(x*4)])

    return (result, result2)

(m1, m2) = maps(lines)

part1 = set()
tobechecked = m1.get("shiny gold")

while len(tobechecked) > 0:
    v = tobechecked.pop()
    part1.add(v)
    tobechecked = tobechecked.union(m1.setdefault(v, set()))

part2 = 0
tobechecked = [("shiny gold", 1)]
while len(tobechecked) > 0:
    (b, count) = tobechecked.pop()
    for (k, v) in m2.setdefault(b, {}).items():
        tobechecked.append((k, count*v))
        part2 += count*v

print("Part1:", len(part1))
print("Part2:", part2)
