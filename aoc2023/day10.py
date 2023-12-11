
from aocd import data, post

input = data.split('\n')

dirs = {
    '|': {(0, 1): (0, 1), (0, -1): (0, -1)},
    '-': {(-1, 0): (-1, 0), (1, 0): (1, 0)},
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
    r = []
    if input[y][x+1] in ('-', 'J', '7'):
        r.append((1, 0))
    if input[y][x-1] in ('-', 'G', 'L'):
        r.append((-1, 0))
    if input[y-1][x] in ('|', '7', 'F'):
        r.append((0, -1))
    if input[y+1][x] in ('|', 'L', 'J'):
        r.append((0, 1))

    r = tuple(r)

    repl = {
        ((1,0), (0, -1)): 'L',
        ((1,0), (0, 1)): 'F'
    }

    return (r[0], repl[r])

(d, repl) = finddir(x, y, input)

pipe = set((x, y))

while True:
    (x, y) = (x+d[0], y+d[1])
    pipe.add((x,y))
    if input[y][x] == 'S':
        break
    d = dirs[input[y][x]][d]

r1 = (len(pipe)-1)//2

post.submit(r1, part="a", day=10)

r2 = 0

straight = {'L': '7', '7': 'L', 'J': 'F', 'F': 'J' }

input[y] = input[y].replace('S', repl)

for yi in range(len(input)):
    crossed = 0
    onpipe = False
    lastcorner = None

    for xi in range(len(input[0])):
        if (xi, yi) in pipe:
            if onpipe:
                if input[yi][xi] in ('L', 'J', 'F', '7'):
                    if input[yi][xi] == straight[lastcorner]:
                        crossed += 1
                    onpipe = False
                    lastcorner = None
            else:
                if input[yi][xi] in ('L', 'J', 'F', '7'):
                    onpipe = True
                    lastcorner = input[yi][xi]
                else:
                    crossed += 1

        elif crossed%2 == 1:
            r2 += 1

post.submit(r2, part="b", day=10)
