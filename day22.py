
import re

filename = "input22.txt"

text_file = open(filename, "r")
lines = text_file.readlines()


REVERT = 1
CUT = 2
DEAL = 3

L = 10007

def commands(lines):
    rr = re.compile("(deal into new stack)|cut (.*)|deal with increment (.*)")

    for l in lines:
        l = l.strip()
        m = rr.match(l)

        if m.group(1) is not None:
            print(l, (REVERT, 0))
            yield (REVERT, 0)            
        elif m.group(2) is not None:
            print(l, (CUT, int(m.group(2))))
            yield (CUT, int(m.group(2)))
        elif m.group(3) is not None:
            print(l, (DEAL, int(m.group(3))))
            yield (DEAL, int(m.group(3)))
        else:
            raise RuntimeError("No match")


pos = 2019+1


for c in commands(lines):
    (c, a) = c

    m = (L // 2) + (L % 2)
    if c == REVERT:
        pos = m + (m - pos) + 1 - (L % 2)
        print("Pos", pos)

    elif c == CUT:
        a = (L + a) % L

        pos = (((pos - 1) + (L - a)) % L) + 1

        print("Pos", pos)

    elif c == DEAL:
        pos = (((pos-1) * a) + 1) % L
        print("Pos", pos)


print("Result 1:", pos - 1, (pos,))