
from itertools import count
cardpk = 11349501
doorpk = 5107328

part1 = 0
for p in count(start=1):
    v = pow(7, p, 20201227) 
    if v == cardpk:
        part1 = pow(doorpk, p, 20201227)
        break
    if v == doorpk:
        part1 = pow(cardpk, p, 20201227)
        break

print("Part1:", part1)


