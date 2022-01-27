text_file = open("input12.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

passages = {}

for l in lines:
    (b, e) = l.split('-')
    passages.setdefault(b, {})[e] = 1
    passages.setdefault(e, {})[b] = 1

def r(last, small, burned, path):
    rc = 0
    for n in passages[last]:
        if n == "end":
            rc += 1
        else:
            if n in small and not burned and n != "start":
                rc += r(n, small, True, path + (n,))

            elif n not in small:
                if n.lower() == n:
                    small.add(n)
                rc += r(n, small, burned, path + (n,))
                if n in small:
                    small.remove(n)
            
    return rc

def calc(allowOne):
    return r('start', set(['start']), not allowOne, ('start',))

print("Part1:", calc(False))

print("Part2:", calc(True))
