from itertools import product
from functools import reduce

text_file = open("input20.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

tiles = {}

nb = {}

def rotate(matrix, ly):
    newm = []
    for x in range(len(matrix)):
        newm.append([matrix[len(matrix) - 1 - ly(y)][x] for y in range(len(matrix))])
    return newm

def middle(matrix):
    return [matrix[ri][1:-1] for ri in range(1,9)]

def left(matrix):
    return ''.join((matrix[ri][0] for ri in range(0, 10)))

def right(matrix):
    return ''.join((matrix[ri][9] for ri in range(0, 10)))

allmatrices = {}
topindex = {}
leftindex = {}

for i in range(len(lines)//12):

    (x, tileno) = lines[i*12].split(' ')
    tileno = int(tileno[:-1])

    matrix = [list(x) for x in lines[i*12+1:i*12+11]]

    allmatrices[tileno] = matrix

    tiles[tileno] = set()

    for x in range(8):
        tiles[tileno].add(right(matrix))
        topindex.setdefault(''.join(matrix[0]), {})[tileno] = (middle(matrix), ''.join(matrix[9]), right(matrix))
        leftindex.setdefault(left(matrix), {})[tileno] = (middle(matrix), ''.join(matrix[9]), right(matrix))
        
        if x == 3:
            matrix = rotate(matrix, lambda y: 9-y)
        else:
            matrix = rotate(matrix, lambda y: y)

for tileno in tiles.keys():
    for tileno2 in set(tiles.keys()).difference([tileno]):
        if len(tiles[tileno2].intersection(tiles[tileno])) > 0:
            nb.setdefault(tileno, set()).add(tileno2)
            nb.setdefault(tileno2, set()).add(tileno)

part1 = reduce(lambda x,y: (x[0].union(y[0]), x[1]*y[1]), [(set([x[0]]), x[0]) for x in filter(lambda x: len(x[1]) == 2, nb.items())], (set(), 1))

print("Part1:", part1[1])
corners = list(part1[0])

mainfield = []
def savetomain(x, y, matrix):
    global mainfield

    for j in range(8):
        yy = y * 8 + j
        if len(mainfield) < yy+1:
            mainfield.append([])
        for i in range(8):
            mainfield[yy].append(matrix[j][i])

start = corners[0]

bigp = []

matrix = allmatrices[start]
while True:
    bottom = ''.join(matrix[9])
    right = ''.join([matrix[x][9] for x in range(10)])
    if len(leftindex[right]) == 2 and len(topindex[bottom]) == 2:
        bigp = [[(right, bottom)]]
        break
    else:
        matrix = rotate(matrix, lambda y: y)

y = 0
x = 1

small = []
for z in range(1, 9):
    small.append(matrix[z][1:-1])

savetomain(0, 0, small)

processed = set([start])

while len(processed) < len(tiles):
    if x == 0:
        (right, bottom) = bigp[y-1][x]
        tileno = list(set(topindex[bottom].keys()).difference(processed))[0]
        (matrix, newbottom, newright) = topindex[bottom][tileno]
        savetomain(x, y, matrix)
        bigp.append([(newright, newbottom)])
        processed.add(tileno)
        x += 1
    else:
        (right, bottom) = bigp[y][x-1]

        s = set(leftindex[right].keys()).difference(processed)
        if len(set(leftindex[right].keys()).difference(processed)) == 1:
            tileno = s.pop()
            (matrix, newbottom, newright) = leftindex[right][tileno]
            savetomain(x, y, matrix)
            bigp[y].append((newright, newbottom))
            processed.add(tileno)

            x += 1
        else:
            x = 0
            y += 1

snakecoord = [(18,0), (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1), (18, 1), (19, 1), (1, 2), (4, 2), (7, 2), (10, 2), (13, 2), (16, 2)]
def detect(mainfield):
    coordtocheck = product(range(len(mainfield[0]) - 19), range(len(mainfield) - 2))
    matchcount = 0
    for c in coordtocheck:
        match = True
        for s in snakecoord:
            match = match and (mainfield[c[1]+s[1]][c[0]+s[0]] == '#')

        matchcount += 1 if match else 0

    return matchcount

hashcount = sum((s.count('#') for s in mainfield))

d = 0
for x in range(8):
    d = detect(mainfield)

    if d > 0:
        break
    if x == 3:
        mainfield = rotate(mainfield, lambda x: len(mainfield) - 1 - x)
    else:
        mainfield = rotate(mainfield, lambda x: x)

print("Part2:", hashcount - len(snakecoord)*d)
