text_file = open("input13.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

dots = {}

def calc(dots, no, d):

    if d == 'x':
        for k in list(dots.keys()):
            if k[0] > no:
                z = k[0] - no
                dots[(no - z, k[1])] = 1
                del dots[k]
            elif k[0] == no:
                del dots[k]
    else:
        for k in list(dots.keys()):
            if k[1] > no:
                z = k[1] - no
                dots[(k[0], no - z)] = 1
                del dots[k]
            elif k[1] == no:
                del dots[k]

    return dots

for l in lines:
    if l == "":
        continue
    elif "," in l:
        c = list(map(int, l.split(',')))
        dots[(c[0],c[1])] = 1
    else:
        no = l.split('=')
        d = no[0].split(' ')[2]
        no = int(no[1])

        dots = calc(dots, no, d)

        break

print("Part1:", len(dots))

dots = {}

for l in lines:
    if l == "":
        continue
    elif "," in l:
        c = list(map(int, l.split(',')))
        dots[(c[0],c[1])] = 1
    else:
        no = l.split('=')
        d = no[0].split(' ')[2]
        no = int(no[1])

        dots = calc(dots, no, d)

x = 0
y = 0

for k in dots.keys():
    if k[0] > x:
        x = k[0]

    if k[1] > y:
        y = k[1]

print("Part2:\n")

for y1 in range(y+1):
    for x1 in range(x+1):
        if (x1, y1) in dots:
            print('#', end='')
        else:
            print(' ', end='')
    print('')


