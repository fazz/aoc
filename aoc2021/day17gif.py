from collections import defaultdict
from math import isqrt
from datetime import datetime
from PIL import Image, ImageDraw, ImageColor

from math import log

tstart = datetime.now()

(x1, x2) = (79,137)
(y2, y1) = (-176,-117)

#(x1, x2) = (20,30)
#(y2, y1) = (-10,-5)

def asum(end, start):
    n = end - start + 1
    return (2*start+n-1)*n // 2

ysteps = defaultdict(list)

ms = isqrt(8*-y2)

for s in range(y2, 1):
    for step in range(ms):
        yy = -asum(-s+step, -s)
        if y2 <= yy <= y1:
            ysteps[step].append(s)
            ysteps[step - 2*(s+1) + 1].append(-s-1)

speeds = set()
cycles = 0
for xspeed in range(x2+1):
    for endstep in range(xspeed+1):
        d = xspeed - endstep
        s = asum(xspeed, d)
        if s > x2:
            break
        elif s >= x1:
            m = (-y2*2) if d == 0 else endstep+1
            for es in range(endstep, m):
                speeds.update([(xspeed, ys) for ys in ysteps[es]])

print("Part2:", len(speeds))
print("Part2 time:", (datetime.now() - tstart).microseconds // 1000, "ms")

imgsc = 3

z = 15400
h = z - y2
w = x2

def l(x):
    b = 1.018
    # pildi kqrgus
    m = int(log(h*imgsc,b))

    return m - int(log(max(1, h*imgsc-x),b))
    return x

def baseimage():
    col = ImageColor.getcolor("hsl(75, 20%, 25%)",'P')
    image = Image.new("P", ((w)*imgsc, 1+l((h)*imgsc)), col)

    draw = ImageDraw.Draw(image)

    hue = 250
    sat = 25
    li = 75
    col = ImageColor.getcolor("hsl(" + str(hue) + ", " + str(sat) + "%, " + str(li) + "%)",'P')

    draw.rectangle((x1*imgsc, l((z-y1)*imgsc), x2*imgsc, l((z-y2)*imgsc)), fill=col)

    return image

def points(speeds):
    sc = 0
    for s in list(speeds):#[0:100]:
        pp = (0,0)
        yield ((pp,pp), pp, sc)
        while pp[1] >= y2:
            (x,y) = (pp[0]+s[0], pp[1]+s[1])
            s = (max(s[0]-1, 0), s[1] - 1)
            if y < y2 or x > x2:
                break
            yield((pp, (x,y)), (x,y), sc)
            pp = (x,y)
        sc += 1

def genframes(prev):
    lines = []
    dots = []

    for (ln, d, n) in points(speeds):
        lines.append(ln)
        dots.append(d)

        if len(dots) % 100 == 0:
            cf = prev.copy()
            draw = ImageDraw.Draw(cf)

            for ln in lines:
                ((lx1,ly1),(lx2,ly2)) = ln
                hue = 50
                sat = 75
                li = 40
                col = ImageColor.getcolor("hsl(" + str(hue) + ", " + str(sat) + "%, " + str(li) + "%)",'P')

                draw.line((lx1*imgsc, l((z-ly1)*imgsc), lx2*imgsc, l((z-ly2)*imgsc)), fill=col)

            for d in dots:
                (x,y) = d
                if x1 <= x <= x2 and y2 <= y <= y1:
                    hue = 20
                    li = 50
                else:
                    hue = 0
                    li = 100
                sat = 100
                col = ImageColor.getcolor("hsl(" + str(hue) + ", " + str(sat) + "%, " + str(li) + "%)",'P')

                draw.rectangle((x*imgsc-imgsc//2, l((z-y)*imgsc)-imgsc//2, x*imgsc+imgsc//2, l((z-y)*imgsc)+imgsc//2), fill=col)

            prev = cf
            yield prev

    #print(dots)
#
#        pp = (0,0)
#        for (x,y) in path:
#            if pp[0] <= x and pp[1] <= y:
#                color = "white"
#            else:
#                color = "red"
#            draw.rectangle((x*imgsc, y*imgsc, (x+1)*imgsc-1, (y+1)*imgsc-1), fill=color)
#            pp = (x,y)
#
#        (x,y) = pos
#        draw.rectangle((x*imgsc, y*imgsc, (x+1)*imgsc-1, (y+1)*imgsc-1), fill="white")
#

def make_gif():
    frames = []

    frames.append(baseimage())

    prev = frames[0]
    for f in genframes(prev):
        frames.append(f)

    frame_one = frames[0]
    frame_one.save("day17.gif", format="GIF", append_images=frames, #transparency=1, disposal=2,
                   save_all=True, duration=1, loop=0)
    
make_gif()