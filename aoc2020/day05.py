import re

text_file = open("input05.txt", "r")
lines = text_file.readlines()

def calcid(spec):
    def c(ch):
        return '0' if ch in ['F', 'L'] else '1'
    return int("".join(list(map(c, spec))), 2)

part1 = 0
allseats = []
for l in lines:
    l = l.rstrip("\n\r")
    r = calcid(l)
    part1 = r if r > part1 else part1
    allseats.append(r)

allseats.sort()

def findhole(input):
    if len(input) == 2:
        return input[0]+1
    low = input[0]
    hi = input[-1]
    pivot = len(input) // 2 + len(input) % 2 - 1
    if input[pivot] > low + pivot:
        return findhole(input[0:pivot+1])
    else:
        return findhole(input[pivot:])

print("Part1:", part1)

print("Part2:", findhole(allseats))
