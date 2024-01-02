
from aocd import data, post
from collections import defaultdict

input = data.split('\n')

dirs = {
    '-': {(1, 0): (1, 0), (-1, 0): (-1, 0)},
    '|': {(0, 1): (0, 1), (0, -1): (0, -1)},
    'L': {(0, 1): (1, 0), (-1, 0): (0, -1)},
    'J': {(1, 0): (0, -1), (0, 1): (-1, 0)},
    '7': {(1, 0): (0, 1), (0, -1): (-1, 0)},
    'F': {(-1, 0): (0, 1), (0, -1): (1, 0)},
}

for yi in range(len(input)):
    if 'S' in input[yi]:
        (x, y) = (input[yi].index('S'), yi)
        break

def finddir(x, y, input):
    r = [startd for d in ((0,1), (1,0), (0,-1), (-1, 0)) for startd in dirs[input[y+d[1]][x+d[0]]] if startd == d]

    for (k,v) in dirs.items():
        if (r[0], (-r[1][0], -r[1][1])) in v.items():
            return (r[0], k)

(d, repl) = finddir(x, y, input)

pipe = set((x, y))

while True:
    (x, y) = (x+d[0], y+d[1])
    pipe.add((x,y))
    if input[y][x] == 'S':
        break
    if input[y][x] in dirs:
        d = dirs[input[y][x]][d]

r1 = (len(pipe)-1)//2

print("r1:", r1)

post.submit(r1, part="a", day=10)

r2 = 0

input[y] = input[y].replace('S', repl)

amounts = defaultdict(int, {'L': 0.5, '7': 0.5, 'F': -0.5, 'J': -0.5, '|': 1})

for yi in range(len(input)):
    crossed = 0

    for xi in range(len(input[0])):
        if (xi, yi) in pipe:
            crossed += amounts[input[yi][xi]]
        elif crossed%2 == 1:
            r2 += 1

print("r2:", r2)

post.submit(r2, part="b", day=10)
