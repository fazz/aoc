
rangestart = 271973
rangeend = 785961

rangestart = 277777
rangeend = 779999

def adj(x):
    while x > 9:

        if (x % 100) % 11 == 0:
            return True
        
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
    if adj(i) and grow(i):
        count = count + 1

print(count)