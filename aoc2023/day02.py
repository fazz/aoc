
from aocd import data, post
import re

input = data.split('\n')

r1 = 0
r2 = 0

limits = { 'red': 12, 'green': 13, 'blue': 14 }

def parse(game):
    (pr, stats) = game.split(': ')
    (_, n) = pr.split(' ')

    n = int(n)

    rt = [(int(count[0]), count[1]) for cube in re.split(r',|;', stats) for count in (cube.split(), )]

    return (n, rt)

for (n, trials) in map(parse, input):

    lowest = { 'red': 0, 'green': 0, 'blue': 0 }

    possible = True

    for (count, color) in trials:
        if count > limits[color]:
            possible = False
        lowest[color] = max(lowest[color], count)

    r1 = r1 + (n if possible else 0)

    r2 += lowest['green']*lowest['red']*lowest['blue']

post.submit(r1, part="a", day=2)
post.submit(r2, part="b", day=2)
