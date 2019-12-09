
from copy import deepcopy

def value(memory, position, mode):
    if mode == 0:
        return memory[memory[position]]
    if mode == 1:
        return memory[position]

def position(memory, position, mode):
    if mode == 0:
        return memory[position]
    if mode == 1:
        raise "Unspecified?"

def cont(memory, pc, input, output):
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
            head, *tail = input
            memory[resultpos] = head
            input = tail

        elif opcode == 4:
            pcinc = 2
            op1 = value(memory, pc+1, p1mode)
            output.append(op1)
            # When output, return
            return (input, output, memory, pc+pcinc)

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

    # Output end marker
    output.append('STOP')

    return (input, output, memory, pc)

# First run from image
def execute(image, input, output):
    memory = image.copy()
    pc = 0
    return cont(memory, pc, input, output)

inputprogram='3,8,1001,8,10,8,105,1,0,0,21,38,63,88,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,102,5,9,9,101,3,9,9,1002,9,3,9,101,3,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,3,9,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,2,9,9,101,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99'

#inputprogram='3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'

#inputprogram='3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

origmemory = [int(x) for x in inputprogram.split(',')]

def simulate(stages, currentmax):
    stage = 0
    # 1st stage gets 0 for starters
    stages[stage][2].append(0)
    while True:
        # stages: memory, PC, input, output

        output = []

        (input, output, memory, pc) = cont(stages[stage][0], stages[stage][1], stages[stage][2], stages[stage][3])

        stages[stage] = (memory, pc, input, output)

        noout = False

        if output[-1] == 'STOP':
            if stage == 4:
                return max(output[-2], currentmax)
            else:
                #raise "Simple STOP out of place?"
                noout = True

        stage = (stage + 1) % 5

        # Push output forward
        if not noout:
            stages[stage][2].append(output[-1])


def permutation(stages, stage, currentmax, options):
    if not len(options):
        return simulate(stages, currentmax)

    for phase in options:
        cstages = deepcopy(stages)
        # memory, PC, input, output
        cstages[stage] = (origmemory.copy(), 0, [phase], [])
        currentmax = permutation(cstages, stage + 1, currentmax, options.difference({phase}))

    return currentmax

    
print(permutation({}, 0, 0, set(range(5,10))))

