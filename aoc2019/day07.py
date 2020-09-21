
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

def execute(image, input, output):

    memory=image.copy()
    
    pc = 0

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

    return (input, output, memory)



inputprogram='3,8,1001,8,10,8,105,1,0,0,21,38,63,88,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,102,5,9,9,101,3,9,9,1002,9,3,9,101,3,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,3,9,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,2,9,9,101,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99'

#inputprogram='3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'

#inputprogram='3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'

#inputprogram='3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'

origmemory = [int(x) for x in inputprogram.split(',')]

def run(phase, inputvalue):
    i = [phase, inputvalue]
    o = []
    (input, output, memory) = execute(origmemory, i, o)
    return output[0]

maxresult = 0

def permutation(currentmax, options, input):
    if not len(options):
        return max(input, currentmax)

    for phase in options:
        output = run(phase, input)
        currentmax = permutation(currentmax, options.difference({phase}), output)

    return currentmax
    
print(permutation(0, set(range(5)), 0))

