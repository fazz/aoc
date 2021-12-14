text_file = open("input14.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

start = lines[0]

rules = {}

for l in lines[2:]:
    r = l.split(' -> ')
    rules[r[0]] = r[1]

def count(pair, exp, cycles):
    exp.setdefault(pair, {})
    if pair in exp and cycles in exp[pair]:
        return exp
    elif pair in rules:
        if cycles == 1:
            exp[pair][cycles] = {pair[0]: 0, rules[pair]: 0}
            exp[pair][cycles][pair[0]] += 1
            exp[pair][cycles][rules[pair]] += 1
        else:
            l = pair[0] + rules[pair]
            exp = count(l, exp, cycles-1)

            r = rules[pair] + pair[1]
            exp = count(r, exp, cycles-1)

            l = exp[l][cycles-1]
            r = exp[r][cycles-1]

            exp[pair][cycles] = {k: l.get(k, 0) + r.get(k, 0) for k in set(r) | set(l)}
    else:
        exp[pair][cycles] = {pair[0]: 1}

    return exp

def calc(cycles):
    # original pair -> cycles -> {} -- count, without the last symbol of the pair
    exp = {}

    for i in range(len(start)):
        exp = count(start[i:i+2], exp, cycles)

    counts = {}
    for z in [exp[pair].get(cycles, {}) for pair in exp.keys()]:
        counts = {k: counts.get(k, 0) + z.get(k, 0) for k in set(counts) | set(z)}
    return max(counts.values()) - min(counts.values())

print("Part1:", calc(10))

print("Part2:", calc(40))
