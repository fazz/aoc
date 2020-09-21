
from random import randrange
from copy import deepcopy

def getmem(memory, position):
    if position > len(memory)-1:
        memory.extend([0] * (1 + position - len(memory)))

    if position < 0:
        raise "Subzero address on read"

    return memory[position]

def setmem(memory, position, value):
    getmem(memory, position)

    if position < 0:
        raise "Subzero address on write"

    memory[position] = value
    return memory

def arraygen(input):
    while len(input) > 0:
        yield input.pop(0)

def arrayplusgen(input, othergen):
    while len(input) > 0:
        yield input.pop(0)
    while True:
        yield next(othergen)

# 0 - position mode
# 1 - immediate mode
# 2 - relative mode
def value(memory, position, mode, rel):
    if mode == 0:
        return getmem(memory, getmem(memory, position))
    if mode == 1:
        return memory[position]
    if mode == 2:
        return getmem(memory, getmem(memory, position) + rel)

def position(memory, position, mode, rel):
    if mode == 0:
        return getmem(memory, position)
    if mode == 1:
        raise "Unspecified?"
    if mode == 2:
        return getmem(memory, position) + rel

def execute(image, inputgenerator):
    memory = image.copy()
    pc = 0
    lastoutput = None
    rel = 0

    while memory[pc] != 99:
        opcode = memory[pc] % 100
        p1mode = (memory[pc] // 100 ) % 10
        p2mode = (memory[pc] // 1000 ) % 10
        p3mode = (memory[pc] // 10000 ) % 10

        if opcode == 1:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode, rel)
            op2 = value(memory, pc+2, p2mode, rel)
            resultpos = position(memory, pc+3, p3mode, rel)
            setmem(memory, resultpos, op1+op2)
            
        elif opcode == 2:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode, rel)
            op2 = value(memory, pc+2, p2mode, rel)
            resultpos = position(memory, pc+3, p3mode, rel)
            setmem(memory, resultpos, op1*op2)

        elif opcode == 3:
            pcinc = 2
            resultpos = position(memory, pc+1, p1mode, rel)
            try:
                ivalue = next(inputgenerator)
            except StopIteration:
                raise RuntimeError("Input not available")
            setmem(memory, resultpos, ivalue)

        elif opcode == 4:
            pcinc = 2
            op1 = value(memory, pc+1, p1mode, rel)
            lastoutput = op1
            yield op1

        elif opcode == 5:
            pcinc = 3
            op1 = value(memory, pc+1, p1mode, rel)
            op2 = value(memory, pc+2, p2mode, rel)
            if op1 != 0:
                pc = op2
                pcinc = 0

        elif opcode == 6:
            pcinc = 3
            op1 = value(memory, pc+1, p1mode, rel)
            op2 = value(memory, pc+2, p2mode, rel)
            if op1 == 0:
                pc = op2
                pcinc = 0

        elif opcode == 7:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode, rel)
            op2 = value(memory, pc+2, p2mode, rel)
            resultpos = position(memory, pc+3, p3mode, rel)
            setmem(memory, resultpos, 1 if op1 < op2 else 0)

        elif opcode == 8:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode, rel)
            op2 = value(memory, pc+2, p2mode, rel)
            resultpos = position(memory, pc+3, p3mode, rel)
            setmem(memory, resultpos, 1 if op1 == op2 else 0)

        elif opcode == 9:
            pcinc = 2
            op1 = value(memory, pc+1, p1mode, rel)
            rel += op1

        else:
            raise "Unknown opcode"
        
        pc = pc+pcinc

    return (memory, lastoutput)


inputprogram='109,424,203,1,21102,11,1,0,1105,1,282,21101,0,18,0,1105,1,259,2101,0,1,221,203,1,21102,1,31,0,1105,1,282,21102,1,38,0,1105,1,259,20102,1,23,2,21201,1,0,3,21102,1,1,1,21102,57,1,0,1106,0,303,2102,1,1,222,21002,221,1,3,20101,0,221,2,21101,0,259,1,21101,0,80,0,1105,1,225,21101,44,0,2,21102,91,1,0,1105,1,303,1202,1,1,223,21002,222,1,4,21102,259,1,3,21102,1,225,2,21102,225,1,1,21101,118,0,0,1106,0,225,21002,222,1,3,21101,163,0,2,21101,0,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,148,1,0,1106,0,259,1202,1,1,223,20101,0,221,4,21001,222,0,3,21102,1,24,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21101,195,0,0,105,1,108,20207,1,223,2,21002,23,1,1,21102,-1,1,3,21102,1,214,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,22102,1,-3,1,22101,0,-2,2,22101,0,-1,3,21102,250,1,0,1106,0,225,21202,1,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22102,1,-2,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21202,-2,1,3,21101,0,343,0,1106,0,303,1106,0,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21101,384,0,0,1105,1,303,1105,1,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21202,1,1,-4,109,-5,2105,1,0'

origmemory = [int(x) for x in inputprogram.split(',')]

input = [0,0]

affected = 0

for y in range(5):
    for x in range(5):
        input = [x,y]
        g = execute(origmemory, arraygen(input))
        o = next(g)
        #print(o, end='')
        affected += o
    #print("")

print(affected)

# Part 2

area = {}

def findspot(x,y):
    if y in area:
        if x in area:
            return area[y][x]

    input = [x,y]
    g = execute(origmemory, arraygen(input))
    area.setdefault(y, {})[x] = next(g)
    return area[y][x]

startx1 = 1000
#starty2 = 1254

starty1 = startx1 * 490 // 1085
#startx2 = starty2 * 14 // 24

def onedge(x1,y1):
    x2 = x1 - 99
    y2 = y1 + 99
    if findspot(x1, y1) == 1 and findspot(x1, y1-1) == 0:
        # upper edge
        if findspot(x2, y2) == 1 and findspot(x2-1, y2) == 0:
            # left edge
            return (0, 0)
        elif findspot(x2, y2) == 0:
            return (1, 0)
        elif findspot(x2-1, y2) == 1:
            return (-1, 0)
    elif findspot(x1, y1) == 0:
        return (0, 1)
    elif findspot(x1, y1-1) == 1:
        return (0, -1)


x = startx1
y = starty1

while True:
    (dx, dy) = onedge(x,y)
    print("Delta", dx, dy, x, y)
    if (dx, dy) == (0,0):
        break
    x += dx
    y += dy

print((x-99)*10000+y)

# 9850490 vale