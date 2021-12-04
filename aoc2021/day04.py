text_file = open("input04.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

randoms = list(map(int, lines.pop(0).split(',')))

boardall = []

# dict of sets
boarddetect = {}

for bn in range(len(lines)//6):
    boarddetect[bn] = []
    boardall.append(set())

    bl = []

    for x in range(5):
        numbers = list(map(int,filter(lambda x: x != '', lines[bn*6+1+x].split(' '))))
        boardall[bn] = boardall[bn].union(set(numbers))
        bl.append(numbers)
        boarddetect[bn].append(set(numbers))

    for r in list(zip(*bl)):
        boarddetect[bn].append(set(r))

def calcscore(boarddetect, last=False):
    crit = len(boarddetect) if last else 1

    chosen = set()
    winningboards = set()
    lastnumber = None
    for rand in randoms:
        chosen.add(rand)

        for bn in boarddetect:
            for s in boarddetect[bn]:
                if len(s.difference(chosen)) == 0 and bn not in winningboards:
                    winningboard = bn
                    lastnumber = rand
                    winningboards.add(bn)
                    break
            if len(winningboards) == crit:
                break
        else:
            continue
        break

    return sum(boardall[winningboard].difference(chosen))*lastnumber

print("Part1: ", calcscore(boarddetect))

print("Part2: ", calcscore(boarddetect, True))
