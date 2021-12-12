text_file = open("input12.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

passages = {}

for l in lines:
    (b, e) = l.split('-')
    passages.setdefault(b, {})[e] = 1
    passages.setdefault(e, {})[b] = 1

def issmall(s):
    return s.lower() == s

def calc(allowOne):
    stack = [(['start'], 'start', set(['start']), not allowOne)]

    complete = set()

    while len(stack) > 0:
        (path, last, small, burned) = stack.pop()

        for n in passages[last]:
            if n in small:
                continue
            
            if issmall(n):
                smalln = small.union([n])
            else:
                smalln = set(small)

            pathn = path + [n]
            if n == "end":
                complete.add(','.join(pathn))
            else:
                if not burned:
                    stack.append((pathn, n, small, True))
                stack.append((pathn, n, smalln, burned))

    return len(complete)

print("Part1:", calc(False))

print("Part2:", calc(True))

