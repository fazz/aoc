
from functools import reduce

text_file = open("input02.txt", "r")

lines = [tuple(x.rstrip("\n\r").split(' ')) for x in text_file.readlines()]

#      P       R       S
f1 = {"B": 0, "A": 1, "C": 2}
#      R       P       S
f2 = {"X": 0, "Y": 1, "Z": 2}

lines = [(f1[x[0]],f2[x[1]]) for x in lines]

# (i[1] + i[0] % 3): 0 - lost, 1 - draw, 2 - win
result1 = reduce(lambda r,i: r + i[1] + 1 + ((i[1] + i[0])%3)*3, lines, 0)

print("Part 1:", result1)

# (i[1] - i[0] % 3): 0 - should pick Rock, 1 - Paper, 2 - Scissors
result2 = reduce(lambda r,i: r + 3*i[1] + (i[1] - i[0])%3 + 1, lines, 0)

print("Part 2:", result2)

