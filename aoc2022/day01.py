
import aocd

lines = [""] + aocd.models.Puzzle(year=2022, day=1).input_data.split('\n') + [""]

ei = [z[1] for z in filter(lambda x: x[0] == "", zip(lines, range(len(lines))))]

cals = sorted([sum(map(int, lines[ei[i]+1:ei[i+1]])) for i in range(len(ei)-1)], reverse = True)

print("Part 1:", cals[0])

print("Part 2:", sum(cals[0:3]))
