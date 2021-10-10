
from copy import deepcopy

text_file = open("input24.txt", "r")
#text_file = open("input24test.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

delta = {"e": (1, 0), "se": (1, -1), "sw": (-1, -1), "w": (-1, 0), "nw": (-1, 1), "ne": (1, 1)}

tiles = {}

for l in lines:
    x = 0
    y = 0
    i = 0
    while i < len(l):

        if l[i] in ['s', 'n']:
            di = l[i:i+2]
            i += 1
        else:
            di = l[i]

        if y % 2 == 0:
            if di in ['nw', 'sw']:
                (x, y) = (x, delta[di][1]+y)
            else:
                (x, y) = (delta[di][0]+x, delta[di][1]+y)
        else:
            if di in ['ne', 'se']:
                (x, y) = (x, delta[di][1]+y)
            else:
                (x, y) = (delta[di][0]+x, delta[di][1]+y)

        i += 1

        if i == len(l):
            if (x, y) in tiles:
                del tiles[(x,y)]
            else:
                tiles[(x,y)] = True

print("Part1:", len(tiles))
    
#
#
#

def newcoord(x, y, di):
    global delta
    if y % 2 == 0:
        if di in ['nw', 'sw']:
            (x, y) = (x, delta[di][1]+y)
        else:
            (x, y) = (delta[di][0]+x, delta[di][1]+y)
    else:
        if di in ['ne', 'se']:
            (x, y) = (x, delta[di][1]+y)
        else:
            (x, y) = (delta[di][0]+x, delta[di][1]+y)
    return (x,y)

for rnd in range(100):

    newtiles = deepcopy(tiles)

    whitetocheck = set()
    for (x,y) in tiles.keys():
        nbcount = 0
        for d in ["e", "se", "sw", "w", "nw", "ne"]:
            (newx, newy) = newcoord(x, y, d)
            if (newx, newy) in tiles:
                nbcount += 1
            else:
                whitetocheck.add((newx, newy))
        if nbcount == 0 or nbcount > 2:
            del newtiles[(x,y)]

    for (x,y) in whitetocheck:
        nbcount = 0
        for d in ["e", "se", "sw", "w", "nw", "ne"]:
            (newx, newy) = newcoord(x, y, d)
            if (newx, newy) in tiles:
                nbcount += 1
        if nbcount == 2:
            newtiles[(x,y)] = True
        
    tiles = newtiles

print("Part2:", len(tiles))
