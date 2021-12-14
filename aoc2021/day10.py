text_file = open("input10.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

pen = {')': 3, ']': 57, '}': 1197, '>': 25137}
sc = {'(': 1, '[': 2, '{': 3, '<': 4}
m = {')': '(', ']': '[', '}': '{', '>': '<'}

score = 0
acscores = []

for l in lines:
    stack = []
    acscore = 0
    for c in l:
        if c not in m:
            stack.append(c)
        elif len(stack) == 0 or stack[-1:][0] != m[c]:
            score += pen[c]
            break
        else:
            p = stack.pop()
    else:
        if len(stack) > 0:
            for s in reversed(stack):
                acscore *= 5
                acscore += sc[s]
            acscores.append(acscore)

print("Part1:", score)

print("Part2:", sorted(acscores)[len(acscores) // 2])

