
inputA = 289
inputB = 629

a = inputA
b = inputB

result1 = 0

for i in range(0, 40000000):
    a = (a*16807) % 2147483647
    b = (b*48271) % 2147483647

    if (a & 0xffff) == (b & 0xffff):
        result1 += 1

print("Part 1:", result1)

def ca(v):
    while True:
        v = (v*16807) % 2147483647
        if (v & 0x3) == 0:
            yield v

def cb(v):
    while True:
        v = (v*48271) % 2147483647
        if (v & 0x7) == 0:
            yield v

result2 = 0

ga = ca(inputA)
gb = cb(inputB)

for i in range(0, 5000000):
    a = next(ga)
    b = next(gb)

    if (a & 0xffff) == (b & 0xffff):
        result2 += 1

print("Part 2:", result2)
