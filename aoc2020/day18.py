text_file = open("input18.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def compute(line, l):

    value = None

    mul = False

    ci = 0
    while ci < len(line):
        c = line[ci]
        if c == ')':
            return (value, ci)
        elif c == '(':
            (term, cin) = compute(line[ci+1:], l+1)
            if value is None:
                value = term
            else:
                value = (value * term) if mul else (value+term)
            ci += cin+1
        elif ord(c) in range(ord('0'), ord('9')+1):
            term = int (c)
            if value is None:
                value = term
            else:
                value = (value * term) if mul else (value+term)
        elif c == '+':
            mul = False
        elif c == '*':
            mul = True

        ci += 1
    return (value, ci)

part1 = 0
for l in lines:
    part1 += compute(l, 0)[0]

print("Part1:", part1, 21993583522852)

#
#
#

def m(l):
    if len(l) == 0:
        return 1
    return l[0]*m(l[1:])

def compute2(line, l):

    value = None
    multerms = []

    ci = 0
    while ci < len(line):
        c = line[ci]
        if c == ')':
            break
        elif c == '(':
            (term, cin) = compute2(line[ci+1:], l+1)
            if value is None:
                value = term
            else:
                value += term
            ci += cin+1
        elif ord(c) in range(ord('0'), ord('9')+1):
            term = int (c)
            if value is None:
                value = term
            else:
                value += term
        elif c == '*':
            mul = True
            multerms.append(value)
            value = None

        ci += 1
    multerms.append(value)
    return (m(multerms), ci)

part2 = 0
for l in lines:
    part2 += compute2(l, 0)[0]

print("Part2:", part2, 122438593522757)
