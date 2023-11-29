
from aocd import data, post
from functools import reduce
import operator

input1 = [31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33]
input2 = "31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33"
size = 256

def knothashround(input, memory, skip):
    pos = 0
    shift = 0
    for l in input:
        memory[pos:pos+l]=list(memory[pos:pos+l])[::-1]
        pos += (l + skip) % size
        skip += 1

        memory = memory[pos:size] + memory[0:pos]
        shift += pos
        pos = 0

    return (memory, shift, skip)

memory = list(range(0, size))

(memory, shift, skip) = knothashround(input1, memory, 0)

print("Part 1:", memory[(-shift)%size]*memory[(-shift+1) % size])

def knothash(input, size):

    memory = list(range(0, size))
    shift = 0
    skip = 0

    cinput2 = list(map(ord, input)) + [17, 31, 73, 47, 23]

    for c in range(64):
        (memory, extrashift, skip) = knothashround(cinput2, memory, skip)
        shift += extrashift

    memory = memory[(-shift)%size:] + memory[0:(-shift)%size]

    hash = [0]*16

    for i in range(16):
        hash[i] = reduce(operator.xor, memory[i*16:i*16+16], 0)
    
    return hash

hashraw = knothash(input2, size)

r2 = ''.join(format(x, '02x') for x in hashraw)

post.submit(r2, part="b", day=10, year=2017)

