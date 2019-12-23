
import re
import itertools

filename = "input22.txt"

text_file = open(filename, "r")
lines = text_file.readlines()


REVERT = 1
CUT = 2
DEAL = 3
RDEAL = 4

L1 = 10007

def commands(lines):
    rr = re.compile("(deal into new stack)|cut (.*)|deal with increment (.*)")

    for l in lines:
        l = l.strip()
        m = rr.match(l)

        if m.group(1) is not None:
            yield (REVERT, 0)            
        elif m.group(2) is not None:
            yield (CUT, int(m.group(2)))
        elif m.group(3) is not None:
            yield (DEAL, int(m.group(3)))
        else:
            raise RuntimeError("No match")

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

micache = {}

def modinv(a, m):
    if a in micache:
        return micache[a]

    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        micache[a] = x % m
        return x % m

def exec(pos, i, L):
    X = 0
    Y = 1

    for c in i:
        (c, a) = c

        m = (L // 2) + 1 - (L % 2)
        if c == REVERT:
            pos = m + (m - pos)
            X = 2*m - X
            Y = (-Y) % L

        elif c == CUT:

            pos = (pos - a) % L
            X = (X - a) % L

        elif c == DEAL:
            pos = (pos * a) % L

            X = (X * a) % L
            Y = (Y * a) % L

        elif c == RDEAL:
            b = modinv(a, L)
            pos = (pos * b) % L

    return (pos, X, Y)

clist = []
for c in commands(lines):
    clist.append(c)


pos = 2019
op = 2019
count = 10
for i in range(count):
    r = exec(pos, clist, L1)
    (pos, x, y) = r

print("Result 1", pos)

##
def calciter(op, count, x, y, L):
    ut = 1 - pow(y, count, L)
    lt = (1 - y) % L
    result = x * (ut * modinv(lt, L)) + pow(y, count, L) * op
    return result % L

result = calciter(op, count, x, y, L1)

print("Result 1", result)

# Part 2

op = 2020
pos = op
L2 = 119315717514047
count = 101741582076661

for i in range(1): #L2-count-1):
    r = exec(pos, clist, L2)
    (pos, x, y) = r
    print("L2:", pos, x, y)

print("Result 2:", op, pos, (pos + 1,))

print("Result 2:", calciter(op, L2-count, x, y, L2))
print("Result 2:", calciter(op, L2-count-1, x, y, L2))
print("Result 2:", calciter(op, L2-count-2, x, y, L2))
print("Result 2:", calciter(op, L2-count-3, x, y, L2))


# 87791869792200 too high
# 42882069328823 too low