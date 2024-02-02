
from aocd import data, post
from aoc import transposestringmatrix, hammingdistance

input = data.split('\n') + ['']

fields = []
tfields = []

f = 0
while f < len(input):
    if '' in input[f:]:
        l = input[f:].index('')
        m = input[f:f+l]
        fields.append(m)
        tfields.append(transposestringmatrix(m))
        f += l+1

def hammings(f):
    return (hammingdistance(v, f[i+1]) for i, v in enumerate(f[:-1]))

def mirrors(f):
    d = dict(enumerate(f))
    h = hammings(f)
    r = [0, 0]
    for i, v in enumerate(h):
        got = True
        onecount = 0
        if v in (0, 1):
            a = i-1
            b = i+2
            while a in d and b in d:
                hd = hammingdistance(f[a], f[b])
                if hd == 1:
                    onecount += 1
                if hd > 1 or onecount > 1:
                    got = False
                    break
                a -= 1
                b += 1
        if got:
            if onecount == 0 and v == 0:
                r[0] = i + 1
            elif onecount == 1 or v == 1:
                r[1] = i + 1

    return tuple(r)

r1 = 0
r2 = 0

for i in range(len(fields)):

    (f1, f2) = mirrors(fields[i])
    (tf1, tf2) = mirrors(tfields[i])
    r1 += 100*f1 + tf1
    r2 += 100*f2 + tf2

print("r1:", r1)
print("r2:", r2)

post.submit(r1, part="a", day=13)
post.submit(r2, part="b", day=13)
