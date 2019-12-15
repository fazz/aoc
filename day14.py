from math import gcd

text_file = open("input14.txt", "r")
lines = text_file.readlines()

def amt(str):
    (a, m) = tuple(str.strip().split(' '))
    return (int(a), m)

prod = {}

for l in lines:
    #3 TGPH, 1 JPFQ, 2 WHWLK, 5 RKVC, 16 DQLH => 9 LJRQ
    (src, dst) = tuple(l.split('=>'))

    (dsta, dstm) = amt(dst)

    prod[dstm] = (dsta, [])

    for s in src.strip().split(','):
        am = amt(s)

        prod[dstm][1].append(am)

fuelprod = prod['FUEL']

generators = {}

required = {}

summa = 0

def oregen():
    global summa
    global required
    while True:
        summa += required['ORE']
        yield required['ORE']

def creategenerator(material, stepsize, srcrules):

    resource = 0

    while True:
        req = required[material]
        if resource-req < 0:
            coef = ((req-resource-1) // stepsize) + 1
            for src in srcrules:
                if not src[1] in generators:
                    g = creategenerator(src[1], prod[src[1]][0], prod[src[1]][1])
                    generators[src[1]] = g
                else:
                    g = generators[src[1]]

                need = src[0]*coef

                required[src[1]] = need

                got = 0
                while got < need:
                    got += next(g)

            resource += stepsize*coef

        if resource-req < 0:
            raise RuntimeError(("oh pask", got))

        resource -= req
        yield req

# Part 1

generators['ORE'] = oregen()

required['FUEL'] = 1

g = creategenerator('FUEL', 1, fuelprod[1])

next(g)

print(summa)

# Part 2

def exec2(reqfuel):
    global summa
    global required
    global generators
    summa = 0
    generators = {}
    generators['ORE'] = oregen()
    required['FUEL'] = reqfuel

    g2 = creategenerator('FUEL', 1, fuelprod[1])

    got = 0
    while got < reqfuel:
        got += next(g2)

    return summa

reserve = None
low = 1100000
high = 1200000
target = 1000000000000

result = None
while True:
    lrs = exec2(low)
    hrs = exec2(high)
    print (low, high)
    print (lrs, hrs)

    if low == high:
        result = low
        break

    if hrs > target and lrs < target:
        reserve = high
        high = low + ((high-low) // 2)
    elif hrs < target:
        low = high
        high = reserve

print(result)
