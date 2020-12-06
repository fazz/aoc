
import re
from functools import reduce

text_file = open("input06.txt", "r")
lines = text_file.readlines()

def count(lines):
    
    answers1 = set()
    answers2 = None

    (result1, result2) = (0, 0)
    
    def reset():
        nonlocal result1, result2, answers1, answers2
        result1 += len(answers1)
        result2 += len(answers2)
        answers1 = set()
        answers2 = None

    for l in lines:
        l = l.rstrip("\n\r")

        if len(l) == 0:
            reset()
        else:
            sl = set(l)
            answers1 = answers1.union(sl)
            answers2 = sl if answers2 is None else answers2.intersection(sl)

    reset()
    return (result1, result2)

(r1, r2) = count(lines)
print("Part1:", r1)
print("Part2:", r2)
