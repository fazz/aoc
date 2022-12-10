
lines = [x.rstrip("\n\r") for x in open("input09.txt", "r")]

def too_far(h1,h2,t1,t2):
    tf = False
    (d1, d2) = (0, 0)
    if abs(h2-t2) > 1 or abs(h1-t1) > 1:
        tf = True
        if (h1-t1) != 0:
            d1 = (h1-t1)//abs(h1-t1)
        if (h2-t2) != 0:
            d2 = (h2-t2)//abs(h2-t2)

    return (tf, d1, d2)

dirs = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1) }

def calc(count):

    tail_visited = set(((0, 0),))
    positions = [(0, 0) for _ in range(count)]

    for l in lines:
        (d, a) = l.split(' ')
        a = int(a)
        (dx, dy) = dirs[d]

        for _ in range(a):
            positions[0] = (positions[0][0]+dx, positions[0][1]+dy)
            for pn in range(1,count):
                (tf, dtx, dty) = too_far(*positions[pn-1], *positions[pn])
                if tf:
                    positions[pn] = (positions[pn][0]+dtx, positions[pn][1]+dty)
                    if pn == count-1:
                        tail_visited.add((positions[pn],))

    return len(tail_visited)

print("Part 1:", calc(2))
print("Part 2:", calc(10))
