
from aocd import data, post

input = data.split('\n')

def calc(pattern, groups):
    global precalc

    if (pattern, groups) in precalc:
        return precalc[(pattern, groups)]

    leftmostgroup = groups[0]

    qm = len([c for c in pattern if c == '?'])

    reqd = sum(groups) - len([c for c in pattern if c == '#'])

    if reqd < 0 or qm < reqd:
        return 0
    elif leftmostgroup == 0:
        return 1
    elif pattern[0] == '.':
        count = calc(pattern[1:], groups)
        precalc[(pattern, groups)] = count
    else:
        pl = len(pattern)
        nl = len(groups)

        fbrokenidx = pattern.find('#')
        if fbrokenidx == -1:
            fbrokenidx = pl

        if nl == 1:
            bbrokenidx = pattern.rfind('#')
            searchrangestart = max(0, bbrokenidx - leftmostgroup + 1)
            searchrangeend = min(fbrokenidx + 1, pl - leftmostgroup + 1)
            g = (0,)
        else:
            searchrangestart = 0
            searchrangeend = min(fbrokenidx+1, pl-nl-sum(groups)+2)
            g = groups[1:]

        count = 0

        for i in range(searchrangestart, searchrangeend):
            if not '.' in pattern[i:i+leftmostgroup] and (i+leftmostgroup == pl or pattern[i+leftmostgroup] != '#'):
                count += calc(pattern[i+leftmostgroup+1:], g)

        precalc[(pattern, groups)] = count

    return count

r1 = 0
r2 = 0

for l in input:
    (p, n) = l.split()
    n = tuple(map(int, n.split(',')))

    p2 = p
    n2 = n

    for _ in range(4):
        p2 = p2 + '?' + p
        n2 = n2 + n

    precalc = {}

    r1 += calc(p,n)
    r2 += calc(p2,n2)

print("r1:", r1)
print("r2:", r2)

post.submit(r1, part="a", day=12)
post.submit(r2, part="b", day=12)
