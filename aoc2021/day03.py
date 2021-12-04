text_file = open("input03.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def mc(oc, size):
    rest = size - oc
    if oc > rest:
        return '1'
    elif oc < rest:
        return '0'
    return '='

def mostcommon(ll):
    ones = [len(tuple(filter(lambda x: x == '1', y))) for y in list(zip(*ll))]

    return list(map(lambda x: mc(x, len(ll)), ones))

cmp = mostcommon(lines)

gamma = int("".join(cmp), 2)

epsilon = gamma ^ ((1 << len(lines[0])) - 1)

print("Part1: ", gamma*epsilon)

def reduce(lines, c, o, z):
    cl = list(lines)
    pos = 0
    while len(cl) > 1:
        cmp = mostcommon(cl)[pos]

        e = lambda x: (x[0], x[1][pos])
        cl = [a[1] for a in filter(lambda x: e(x) == ('=', c) or e(x) == ('1', o) or e(x) == ('0', z), [(cmp, y) for y in cl])]

        pos += 1

    return int(cl[0], 2)

o2 = reduce(lines, '1', '1', '0')
co2 = reduce(lines, '0', '0', '1')

print("Part2: ", o2*co2)
