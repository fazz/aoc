text_file = open("input05.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

memory = list(map(int, lines))

result1 = 0
pc = 0

while True:
    opc = pc
    pc += memory[pc]
    result1 += 1
    if pc < 0 or pc >= len(memory):
        break
    memory[opc] += 1

print("Part 1:", result1)

memory = list(map(int, lines))

result2 = 0
pc = 0

while True:
    opc = pc
    offset = memory[pc]
    pc += offset
    result2 += 1
    if pc < 0 or pc >= len(memory):
        break
    if offset >= 3:
        memory[opc] -= 1
    else:
        memory[opc] += 1

print("Part 2:", result2)
