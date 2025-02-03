
import aocd

lines = [x.split(' ') for x in aocd.models.Puzzle(year=2022, day=2).input_data.split('\n')]

f = {"X": 1, "Y": 2, "Z": 3}

w = {
    "A": {"X": 3, "Y": 6, "Z": 0},
    "B": {"X": 0, "Y": 3, "Z": 6},
    "C": {"X": 6, "Y": 0, "Z": 3}
}

result1 = 0

for (m1, m2) in lines:
    result1 += f[m2] + w[m1][m2]

print("Part 1:", result1)

det = {"X": 0, "Y": 3, "Z": 6}

result2 = 0

for (m1, m2) in lines:
    for (m3,v) in w[m1].items():
        if v == det[m2]:
            break

    result2 += f[m3] + w[m1][m3]

print("Part 2:", result2)

