from collections import Counter

text_file = open("input06.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def c(d):
    f = Counter(map(int, lines[0].split(',')))
    for i in range(d):
        f.setdefault(7,0)
        f.setdefault(9,0)
        for k in sorted(f.keys()):
            f.setdefault(k,0)
            if k == 0:
                f[7] += f[0]
                f[9] += f[0]
                del f[0]
            else:
                f[k-1] = f[k]
                del f[k]
    return sum(f.values())

print("Part1:", c(80))
print("Part2:", c(256))