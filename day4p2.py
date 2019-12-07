
rangestart = 271973
rangeend = 785961

rangestart = 277777
rangeend = 779999

def limited(x):
    blocks = {}
    anumber = x % 10
    apos = 0
    pos = 0
    while x > 0:
        blocks[apos] = blocks.setdefault(apos, 0) + 1

        pos = pos + 1
        x = x // 10
        if x % 10 != anumber:
            apos = pos
            anumber = x % 10

    return len(list(filter(lambda x: x == 2, blocks.values()))) > 0

def adj(inp):
    x = inp
    while x > 9:

        if (x % 100) % 11 == 0:
            return limited(x)
        
        x = x // 10

    return False


def grow(x):
    c = 9
    while x > 0:
        if x % 10 > c:
            return False
        c = x % 10
        x = x // 10
    
    return True


count = 0

for i in range(rangestart, rangeend+1):
    if grow(i) and limited(i):
        count = count + 1

print(count)