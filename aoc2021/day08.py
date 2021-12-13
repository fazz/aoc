
text_file = open("input08.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

count = 0

for l in lines:
    sgmt = l.split(' | ')[1].split(' ')
    count += len(list(filter(lambda x: len(x) in[2, 3, 4, 7], sgmt)))

print("Part1:", count)

result = 0

for l in lines:

    ntos = {}
    values = {}

    sp = l.split(' | ')

    test = list(map(tuple, map(sorted, sp[0].split(' '))))
    read = list(map(tuple, map(sorted, sp[1].split(' '))))

    total = test + read

    while len(set(read).difference(values.keys())) > 0:
        for sgmt in total:
            if len(sgmt) == 2:
                values[sgmt] = 1
                ntos[1] = set(sgmt)
            elif len(sgmt) == 3:
                values[sgmt] = 7
                ntos[7] = set(sgmt)
            elif len(sgmt) == 4:
                values[sgmt] = 4
                ntos[4] = set(sgmt)
            elif len(sgmt) == 7:
                values[sgmt] = 8
                ntos[8] = set(sgmt)
            elif len(sgmt) == 5: # 3,5,2
                if 3 not in ntos and 7 in ntos and ntos[7].intersection(sgmt) == ntos[7]:
                    values[sgmt] = 3
                    ntos[3] = set(sgmt)
                elif 7 in ntos and ntos[7].intersection(sgmt) != ntos[7]: # 5, 2
                    if 9 in ntos and ntos[9].intersection(sgmt) == set(sgmt):
                        values[sgmt] = 5
                        ntos[5] = set(sgmt)
                    elif 6 in ntos and ntos[6].intersection(sgmt) == set(sgmt):
                        values[sgmt] = 5
                        ntos[5] = set(sgmt)
                    elif 3 in ntos and 5 in ntos:
                        values[sgmt] = 2
                        ntos[2] = set(sgmt)
            else: # len == 6: 0, 9, 6
                if 4 in ntos and ntos[4].intersection(sgmt) == ntos[4]:
                    values[sgmt] = 9
                    ntos[9] = set(sgmt)
                elif 9 in ntos and set(sgmt) != ntos[9]: # 6 vqi 0
                    if 7 in ntos and ntos[7].intersection(sgmt) == ntos[7]:
                        values[sgmt] = 0
                        ntos[0] = set(sgmt)
                    elif 1 in ntos and ntos[1].intersection(sgmt) == ntos[1]:
                        values[sgmt] = 0
                        ntos[0] = set(sgmt)
                    elif 1 in ntos or 7 in ntos:
                        values[sgmt] = 6
                        ntos[6] = set(sgmt)

    m = 1000
    r = 0
    for z in read:
        r += values[z]*m
        m = m // 10
    result += r

print("Part2:", result)

