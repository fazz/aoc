
from functools import reduce

text_file = open("input03.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def score(c):
    return (ord(c) - ord('a') + 1) if c >= 'a' and c <= 'z' else (ord(c) - ord('A') + 27)

result1 = reduce(lambda r, l: r + score(set(l[0:len(l)//2]).intersection(set(l[len(l)//2:])).pop()), lines, 0)

print("Part 1:", result1)

result2 = reduce(lambda r, i: r + score(set(lines[i*3]).intersection(lines[i*3+1]).intersection(lines[i*3+2]).pop()), range(len(lines)//3), 0)

print("Part 2:", result2)
