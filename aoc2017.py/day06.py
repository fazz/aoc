text_file = open("input06.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

memory = list(map(int, lines[0].split('\t')))

def calc(memory):
    states = set()
    states.add(tuple(memory))
    result = 0
    while True:
        max = -1
        maxi = 0
        for i in range(len(memory)-1, -1, -1):
            if memory[i] >= max:
                max = memory[i]
                maxi = i

        memory[maxi] = 0
        i = maxi
        while max > 0:
            i = (i + 1) % len(memory)
            memory[i] += 1
            max -= 1

        result += 1
        t = tuple(memory)
        if t in states:
            break
        states.add(t)
    return (result, memory)

(r, memory) = calc(memory)
print("Part 1:", r)

(r, memory) = calc(memory)
print("Part 2:", r)

