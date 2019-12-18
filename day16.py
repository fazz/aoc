
from math import factorial

inputstr = '59705379150220188753316412925237003623341873502562165618681895846838956306026981091618902964505317589975353803891340688726319912072762197208600522256226277045196745275925595285843490582257194963750523789260297737947126704668555847149125256177428007606338263660765335434914961324526565730304103857985860308906002394989471031058266433317378346888662323198499387391755140009824186662950694879934582661048464385141787363949242889652092761090657224259182589469166807788651557747631571357207637087168904251987880776566360681108470585488499889044851694035762709053586877815115448849654685763054406911855606283246118699187059424077564037176787976681309870931'

inp = [int(i) for i in list(str(inputstr))]
offset = int(inputstr[0:7])

size = len(inp)
lsize = size*10000

# Part 1

# 1-based
def gen(row, pos):
    elements = [0, 1, 0, -1]

    return elements[(pos // row) % 4]

def part1(cstate):
    for x in range(100):
        state = []
        for y in range(1, size+1):
            state.append(0)
            for x in range(y, size+1):
                state[-1] += cstate[x-1]*gen(y, x)

        cstate = [abs(z) % 10 for z in state]

    return cstate

#print("Result 1", ''.join([str(z) for z in part1(inp)[0:8]]))

# Part 2

output = [0] * 8

rounds = 100

def bc(n, k):
    a = factorial(n)
    b = factorial(k)
    z = n - k
    div = a // (b * factorial(z))
    while True:
        yield div

        n += 1
        z += 1
        div = (div * n) // z

coef = [None] * (lsize-offset)

print(lsize-offset)
g = bc(rounds-1, rounds-1)
for i in range(lsize-offset):
    coef[i] = next(g)

for o in range(8):
    for c in range(lsize-offset-o):
        output[o] = output[o] + (inp[(offset+o+c) % size]*coef[c])

output = [o % 10 for o in output]

print("Result 2", ''.join([str(z) for z in output]))
