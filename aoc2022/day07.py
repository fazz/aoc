
from functools import reduce

text_file = open("input07.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

dir = {"/": ("None", "D", {})}

curdir = dir["/"]

for l in lines:
    c = l.split(' ')

    if c[0] == "$":
        if c[1] == "ls":
            pass
        elif c[2] == "..":
            curdir = curdir[0]
        elif c[2] == "/":
            curdir = dir["/"]
        else:
            curdir[2].setdefault(c[2], (curdir, "D", {}))
            curdir = curdir[2][c[2]]
    else:
        if not c[0] == "dir":
            curdir[2][c[1]] = (curdir, "F", int(c[0]))

def sumx(d, limit, checker):
    result = 0
    for e in d[2].values():
        if e[1] == "D":
            for (inter, s) in sumx(e, limit, checker):
                if checker(s,limit):
                    yield (True, s)
                if not inter:
                    result += s
        else:
            result += e[2]
    yield (False, result)

result1 = 0
requiredspace = -40000000

for (inter, s) in sumx(dir["/"], 100000, lambda a,b: a<=b):
    if s <= 100000:
        result1 += s
    if not inter:
        requiredspace += s

print("Part 1:", result1)

print("Part 2:", min(reduce(lambda r,i: r.union({i[1]}),sumx(dir["/"], requiredspace, lambda a,b: a>=b), set())))
