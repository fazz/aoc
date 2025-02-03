
from aocd import data, post
from itertools import pairwise
import networkx as nx

input = data.split('\n')

def compute_positive_polygon_area(vert):
    area = compute_polygon_area(vert)
    if area >= 0:
        return area
    # if the vertices were not given in counter-clockwise order,
    # the result will be negative
    return -area

def compute_polygon_area(vert):
    area = 0

    # Triangle formula to compute area of a polygon
    # https://en.m.wikipedia.org/wiki/Shoelace_formula#Triangle_formula
    for (x1, y1), (x2, y2) in pairwise(vert + [vert[0]]):
        area += x1 * y2 - x2 * y1

    return area / 2

def compute_points_inside_polygon(area, num_edges):
    # Pick's theorem to compute the inner points of a grid-based polygon
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return int(area - num_edges / 2 + 1)

def calc(pf):

    edgesize = 1
    (x,y) = (0,0)

    G = nx.DiGraph()
    G.add_node((x,y))

    for li in range(len(input)):
        (d, n) = pf(input[li])

        if li == len(input) - 1:
            G.add_edge((x, y), (0, 0))
            edgesize += abs(x) + abs(y) - 1
            break

        (ox, oy) = (x, y)
        edgesize += int(n)

        x += n*d[0]
        y += n*d[1]

        G.add_node((x, y))
        G.add_edge((ox, oy), (x, y))

    cycle = [u for u, v in nx.find_cycle(G, (0,0))]

    a = compute_positive_polygon_area(cycle)
    b = compute_points_inside_polygon(a, edgesize)

    return b + edgesize

ds1 = {'R': (1, 0), 'L': (-1, 0), 'D': (0, 1), 'U': (0, -1)}

def p1parse(l):
    (dm, n, _) = l.split()
    d = ds1[dm]
    return (d, int(n))

r1 = calc(p1parse)

print("r1:", r1)

post.submit(r1, part="a", day=18)


ds2 = {0:(1, 0), 1:(0, 1), 2:(-1, 0), 3:(0, -1)}

def p2parse(l):
    (_, _, z) = l.split()
    return (ds2[int(z[7:8])], int(z[2:7], base = 16))

r2 = calc(p2parse)

print("r2:", r2)

post.submit(r2, part="b", day=18)
