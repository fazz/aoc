text_file = open("input02.txt", "r")
lines = text_file.readlines()

part1 = 0
part2 = 0

for l in lines:
    l = l.strip()
    (rule, char, password) = l.split()
    char = char[0]

    (lower, upper) = rule.split('-')

    (lower, upper) = (int(lower), int(upper))

    count = password.count(char)
    if count <= upper and count >= lower:
        part1 += 1

    # part2

    count2 = password.count(char, lower-1, lower) + password.count(char, upper-1, upper)
    if count2 == 1:
        part2 += 1

print("Part1:", part1)
print("Part2:", part2)
