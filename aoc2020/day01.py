
text_file = open("input01.txt", "r")
lines = text_file.readlines()

numbers = []

for l in lines:
    l = l.strip()
    if len(l) > 4:
        continue
    numbers.append(int(l))

result = None

for n1 in numbers:
    if result != None:
        break
    for n2 in numbers:
        if result != None:
            break
        if n1 == n2:
            continue
        if n1+n2 == 2020:
            result = (n1, n2)

(n1, n2) = result

print("Part1: ", n1*n2)

result = None

for n1 in numbers:
    if result != None:
        break
    for n2 in numbers:
        if result != None:
            break
        if n1 == n2:
            continue
        for n3 in numbers:
            if result != None:
                break
            if n3 == n2 or n3 == n1:
                continue
            if n1+n2+n3 == 2020:
                result = (n1, n2, n3)


(n1, n2, n3) = result

print("Part1: ", n1*n2*n3)
