
import copy
from itertools import product

text_file = open("input11.txt", "r")

seats = [(lambda a: list(a))(x.rstrip("\n\r")) for x in text_file.readlines()]

seats2 = copy.deepcopy(seats)

def surrcount(seats, r, c, distance):
    ret = 0
    for (dc, dr) in set(product([-1, 0, 1], [-1, 0, 1])).difference([(0,0)]):
        for i in range(1, distance+1):
            if not 0 <= r + (dr*i) < len(seats):
                break
            if not 0 <= c + (dc*i) < len(seats[r]):
                break

            if seats[r+(dr*i)][c+(dc*i)] == '#':
                ret += 1
                break
            elif seats[r+(dr*i)][c+(dc*i)] == 'L':
                break
    return ret

def calc(seats, sittertolerance, distance):
    sittercount = 0

    prevsittercount = -1

    while sittercount != prevsittercount:
        newseats = copy.deepcopy(seats)

        prevsittercount = sittercount

        for i in range(len(seats)):
            for j in range(len(seats[i])):
                if seats[i][j] == '.':
                    continue
                c = surrcount(seats, i, j, distance)
                if c == 0 and seats[i][j] == 'L':
                    newseats[i][j] = '#'
                    sittercount += 1
                elif c >= sittertolerance and seats[i][j] == '#':
                    newseats[i][j] = 'L'
                    sittercount -= 1
        seats = newseats
    return sittercount

print("Part1:", calc(copy.deepcopy(seats), 4, 1))
print("Part2:", calc(seats, 5, len(seats[0])))
