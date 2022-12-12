
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageDraw, ImageColor

t1 = datetime.now()

text_file = open("input15.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

dim = len(lines)

field = {}
for y in range(dim):
    for x in range(dim):
        field[(x,y)] = int(lines[y][x])

def get(k):
    (x,y) = k
    xc = x // dim
    x = x % dim
    yc = y // dim
    y = y % dim
    return ((field[(x,y)] + xc + yc - 1) % 9) + 1

def nexts(p,m,q):
    (x,y) = p
    u = set()

    if x > 0:
        u.add((x-1, y))

    if y > 0:
        u.add((x, y-1))

    if x < dim*m-1:
        u.add((x+1, y))

    if y < dim*m-1:
        u.add((x, y+1))

    return u.intersection(q)

def compute(m):
    dist = defaultdict(lambda: (dim+dim)*10*m)
    distmap = defaultdict(set)
    dist[(0,0)] = 0
    distmap[0] = set([(0,0)])
    prev = {(0,0):[]}

    maxtaxidist = 0

    q = {(x,y) for x in range(100*m) for y in range(100*m)}
    visited = set()

    while len(q) > 0:
        pos = distmap[min(distmap)].pop()
        if pos[0]+pos[1] > maxtaxidist:
            maxtaxidist = sum(pos)
            yield (pos, prev[pos], visited)

        if len(distmap[min(distmap)]) == 0:
            del distmap[min(distmap)]
        if pos not in q:
            continue
        q.remove(pos)
        visited.add(pos)

        nx = nexts(pos,m,q)

        for n in nx:
            alt = dist[pos] + get(n)
            if alt < dist[n]:
                dist[n] = alt
                prev[n] = prev[pos] + [pos]
                distmap[alt].add(n)

    print("Part1:", dist[(99,99)])
    print("Part2:", dist[(499,499)])

m = 5
imgsc = 1
imgsz = dim*m

def baseimage():
    image = Image.new("P", (imgsz*imgsc, imgsz*imgsc))

    draw = ImageDraw.Draw(image)

    for x in range(imgsz):
        for y in range(imgsz):
            v = get((x,y))
            hue = 250 + (36 * v // 9)
            sat = 25 + (75 * v // 9)
            li = 25 + (50 * v // 9)
            col = ImageColor.getcolor("hsl(" + str(hue) + ", " + str(sat) + "%, " + str(li) + "%)",'P')
            draw.rectangle((x*imgsc, y*imgsc, (x+1)*imgsc-1, (y+1)*imgsc-1), fill=col)
    
    return image

def genframes(prev):
    count = -1
    skip = 15
    for (pos, path, visited) in compute(m):

        count += 1

        if (not count % skip == 0) and pos != (dim*m-1, dim*m-1):
            continue

        cf = prev.copy()

        draw = ImageDraw.Draw(cf)

        for (x,y) in visited.difference(path):

            taxidist = x+y
            maxtaxidist = 2*dim*m

            hue = 10 + (170 * taxidist // maxtaxidist)
            sat = 50
            li = 50
            col = ImageColor.getcolor("hsl(" + str(hue) + ", " + str(sat) + "%, " + str(li) + "%)",'P')

            draw.rectangle((x*imgsc, y*imgsc, (x+1)*imgsc-1, (y+1)*imgsc-1), fill=col)

        pp = (0,0)
        for (x,y) in path:
            if pp[0] <= x and pp[1] <= y:
                color = "white"
            else:
                color = "red"
            draw.rectangle((x*imgsc, y*imgsc, (x+1)*imgsc-1, (y+1)*imgsc-1), fill=color)
            pp = (x,y)

        (x,y) = pos
        draw.rectangle((x*imgsc, y*imgsc, (x+1)*imgsc-1, (y+1)*imgsc-1), fill="white")

        prev = cf
        yield prev

def make_gif():
    frames = []

    frames.append(baseimage())

    prev = frames[0]
    for f in genframes(prev):
        frames.append(f)

    frame_one = frames[0]
    frame_one.save("day15.gif", format="GIF", append_images=frames, #transparency=1, disposal=2,
                   save_all=True, duration=1, loop=0)
    
make_gif()