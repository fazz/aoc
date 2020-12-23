
def calc(size, rounds, input):
    buffer0 = [int(input[x])-1 for x in range(len(input))] + [x for x in range (len(input), size)]
    buffer1 = [x%size for x in range(1, len(input)+1)] + [x%size for x in range (len(input)+1, size+1)]

    cl = buffer0[0]
    cpos = 0

    head = 0
    tail = 0
    picked = [0, 0, 0]
    for rnd in range(rounds):

        z = cpos
        for x in range(3):
            z = buffer1[z]
            picked[x] = buffer0[z]
            tail = z

        head = buffer1[cpos]

        m = 1
        dpos = None
        while True:
            dl = (cl - m) % size
            if dl in picked:
                m += 1
                continue
            if dl < 9:
                dpos = buffer0.index(dl)
            else:
                dpos = dl
            break

        buffer1[cpos] = buffer1[tail]
        cpos = buffer1[tail]
        cl = buffer0[cpos]

        buffer1[tail] = buffer1[dpos]

        buffer1[dpos] = head

    return (buffer0, buffer1)

input = "389125467"
input = "219748365"

(buffer0, buffer1) = calc(9, 100, input)
pos = buffer1[buffer0.index(0)]

res = 0
for x in range(8):
    res = res*10 + buffer0[pos] + 1
    pos = buffer1[pos]

print("Part1:", res, 35827964)

(buffer0, buffer1) = calc(1000000, 10000000, input)
pos = buffer1[buffer0.index(0)]
a = buffer0[pos] + 1
b = buffer0[buffer1[pos]] + 1

print("Part2:", a*b, 5403610688)
