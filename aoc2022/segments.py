
def on_segment(s, point):
    # p, q, r
    (end1, end2) = s
    (x1, y1) = end1
    (x2, y2) = end2
    (x, y) = point

    if x <= max(x1, x2) and x >= min(x1, x2) and y <= max(y1, y2) and y >= min(y1, y2):
        return True
    return False
    
def direction(end1, end2, point):
    (x1, y1) = end1
    (x2, y2) = end2
    (x, y) = point

    val = (y2 - y1) * (x - x2) - (x2 - x1) * (y - y2)
    if val == 0:
        return 0 # collinear
    return 1 if val > 0 else 2 # direction: 1-cw, 2-ccw

def parameters(s):
    ((x1, y1), (x2, y2)) = s
    slope = (y2 - y1) // (x2 - x1)
    return (-slope, y1 - slope*x1)

# assumes crossing at the right angle, diagonally
def find_intersection(s1, s2):
    (a1, c1) = parameters(s1)
    (a2, c2) = parameters(s2)

    x = (c1 - c2) // (a1 - a2)
    y = (a1*c2 - a2*c1) // (a1 - a2)

    return (x,y)

def intersect(s1, s2):
 #   bool loikuvad(Point p1, Point q1, Point p2, Point q2)

    o1 = direction(*s1, s2[0])
    o2 = direction(*s1, s2[1])
    o3 = direction(*s2, s1[0])
    o4 = direction(*s2, s1[1])

    # intersect
    if o1 != o2 and o3 != o4:
        return (True, False, find_intersection(s1, s2))

    # p1, q1 ja p2 on kollineaarsed ja p2 asub lõigul (p1,q1)
    if o1 == 0 and on_segment(s1, s2[0]):
        return (True, True, None)

    # p1, q1 ja q2 on kollineaarsed ja q2 asub lõigul (p1,q1)
    if o2 == 0 and on_segment(s1, s2[1]):
        return (True, True, None)

    # p2, q2 ja p1 on kollineaarsed ja p1 asub lõigul (p2,q2)
    if o3 == 0 and on_segment(s2, s1[0]):
        return (True, True, None)

    # p2, q2 ja q1 on kollineaarsed ja q1 asub lõigul (p2,q2)
    if o4 == 0 and on_segment(s2, s1[1]):
        return (True, True, None)

    return (False, False, None)
    