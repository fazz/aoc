
from PIL import Image, ImageDraw, ImageColor

lines = [x.rstrip("\n\r") for x in open("input09.txt", "r")]

minx = 0
maxx = 0
miny = 0
maxy = 0

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
    global minx, maxx, miny, maxy
    tail_visited = set(((0, 0),))
    positions = [(0, 0) for _ in range(count)]

    for l in lines:
        (d, a) = l.split(' ')
        a = int(a)
        (dx, dy) = dirs[d]

        for _ in range(a):
            positions[0] = (positions[0][0]+dx, positions[0][1]+dy)
            minx = min(positions[0][0], minx)
            maxx = max(positions[0][0], maxx)
            miny = min(positions[0][1], miny)
            maxy = max(positions[0][1], maxy)
            for pn in range(1,count):
                (tf, dtx, dty) = too_far(*positions[pn-1], *positions[pn])
                if tf:
                    positions[pn] = (positions[pn][0]+dtx, positions[pn][1]+dty)
                    if pn == count-1:
                        tail_visited.add((positions[pn],))

    return len(tail_visited)


print("Part 2:", calc(10))


m = 5
imgsc = 3
imgsz = 10*m

def baseimage():
    global minx, maxx, miny, maxy
    print(minx, maxx, miny, maxy)
    image = Image.new("P", (abs(maxx-minx)*imgsc, abs(maxy-miny)*imgsc))

    draw = ImageDraw.Draw(image)

    v = 5
    hue = 250 + (36 * v // 9)
    sat = 25 + (75 * v // 9)
    li = 25 + (50 * v // 9)
    col = ImageColor.getcolor("hsl(" + str(hue) + ", " + str(sat) + "%, " + str(li) + "%)",'P')

    draw.rectangle((0, 0, abs(maxx-minx)*imgsc, abs(maxy-miny)*imgsc), fill=col)
    
    return image


def make_gif():
    frames = []

    frames.append(baseimage())

    prev = frames[0]
    #for f in genframes(prev):
    #    frames.append(f)

    frame_one = frames[0]
    frame_one.save("day09.gif", format="GIF", append_images=frames, #transparency=1, disposal=2,
                   save_all=True, duration=1, loop=0)
    
make_gif()




