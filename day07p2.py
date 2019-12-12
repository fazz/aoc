
from itertools import permutations
from copy import deepcopy

def value(memory, position, mode):
    if mode == 0:
        return memory[memory[position]]
    if mode == 1:
        return memory[position]

def position(memory, position, mode):
    if mode == 0:
        return memory[position]

def execute(image, inputgenerator):
    memory = image.copy()
    pc = 0
    lastoutput = None

    while memory[pc] != 99:
        opcode = memory[pc] % 100
        p1mode = (memory[pc] // 100 ) % 10
        p2mode = (memory[pc] // 1000 ) % 10
        p3mode = (memory[pc] // 10000 ) % 10

        if opcode == 1:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode)
            op2 = value(memory, pc+2, p2mode)
            resultpos = position(memory, pc+3, p3mode)
            memory[resultpos] = op1+op2
            
        elif opcode == 2:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode)
            op2 = value(memory, pc+2, p2mode)
            resultpos = position(memory, pc+3, p3mode)
            memory[resultpos] = op1*op2

        elif opcode == 3:
            pcinc = 2
            resultpos = position(memory, pc+1, p1mode)
            try:
                ivalue = next(inputgenerator)
            except StopIteration:
                raise RuntimeError("Input not available")
            memory[resultpos] = ivalue

        elif opcode == 4:
            pcinc = 2
            op1 = value(memory, pc+1, p1mode)
            lastoutput = op1
            yield op1

        elif opcode == 5:
            pcinc = 3
            op1 = value(memory, pc+1, p1mode)
            op2 = value(memory, pc+2, p2mode)
            if op1 != 0:
                pc = op2
                pcinc = 0

        elif opcode == 6:
            pcinc = 3
            op1 = value(memory, pc+1, p1mode)
            op2 = value(memory, pc+2, p2mode)
            if op1 == 0:
                pc = op2
                pcinc = 0

        elif opcode == 7:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode)
            op2 = value(memory, pc+2, p2mode)
            resultpos = position(memory, pc+3, p3mode)
            memory[resultpos] = 1 if op1 < op2 else 0

        elif opcode == 8:
            pcinc = 4
            op1 = value(memory, pc+1, p1mode)
            op2 = value(memory, pc+2, p2mode)
            resultpos = position(memory, pc+3, p3mode)
            memory[resultpos] = 1 if op1 == op2 else 0

        else:
            raise "Unknown opcode"
        
        pc = pc+pcinc

    return (memory, lastoutput)

inputprogram='3,8,1001,8,10,8,105,1,0,0,21,38,63,88,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,102,5,9,9,101,3,9,9,1002,9,3,9,101,3,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,3,9,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,2,9,9,101,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99'

origmemory = [int(x) for x in inputprogram.split(',')]

def arraygen(input):
    while len(input) > 0:
        yield input.pop(0)

def arrayplusgen(input, othergen):
    while len(input) > 0:
        yield input.pop(0)
    while True:
        yield next(othergen)

def simulate(stages):

    feedback = [stages[4].phase, 0]

    executor = execute(origmemory, arrayplusgen([stages[0].phase],
                    execute(origmemory, arrayplusgen([stages[1].phase],
                        execute(origmemory, arrayplusgen([stages[2].phase],
                            execute(origmemory, arrayplusgen([stages[3].phase],
                                execute(origmemory, arraygen(feedback))
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    try:
        while True:
            v = next(executor)
            feedback.extend([v])
    except StopIteration as ex:
        return ex.value[1]

class Stage:
    def __init__(self, phase):
        self.phase = phase

print(max([simulate(p) for p in permutations([Stage(x) for x in range(5,10)])]))
