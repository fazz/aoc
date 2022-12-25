
lines = [x.rstrip(" \n\r") for x in open("input25.txt", "r")]

summa = 0

conv1 = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}

for l in map(list, lines):
    r = 1
    while len(l) > 0:
        summa += conv1[l.pop()]*r
        r *= 5

r = 0
while 5**r < summa//5:
    r += 1
r = 5**r

buffer = [0]

while r > 0:
    v = summa // r
    buffer.append(v)
    i = len(buffer) - 1
    while buffer[i] > 2:
        buffer[i] = buffer[i]-5
        buffer[i-1] += 1
        i -= 1
    summa = summa % r
    r = r // 5

conv2 = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}

result1 = ''.join(map(lambda x: conv2[x], buffer)).lstrip('0')

print("Part 1:", result1)
