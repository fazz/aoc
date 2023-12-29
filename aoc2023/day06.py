
from aocd import data, post
from math import sqrt


input = data.split('\n')

input = [map(int, x.split(':')[1].split()) for x in input]

input = list(zip(input[0], input[1]))

r1 = 1

def calc(time, distance):

    x1 = ((-time) - sqrt(time*time - 4*distance)) / (-2)
    x2 = ((-time) + sqrt(time*time - 4*distance)) / (-2)

    if x1 == int(x1):
        x1 = int(x1) - 1

    return int(x1) - int(x2)

for (time, distance) in input:

    r1 = r1*calc(time, distance)

post.submit(r1, part="a", day=6)

r2 = 0

ts = ""
ds = ""

for v in input:
    ts += str(v[0])
    ds += str(v[1])

r2 = calc(int(ts), int(ds))

post.submit(r2, part="b", day=6)
