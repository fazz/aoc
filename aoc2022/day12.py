
from collections import defaultdict

lines = [x.rstrip("\n\r") for x in open("input12.txt", "r")]

height = len(lines)
width = len(lines[0])

paths = defaultdict(lambda: set())

q = set()
lowest = set()

for x in range(width):
    for y in range(height):
        q.add((x,y))
        vector = (1,0)
        for _ in range(4):
            
            (nx, ny) = (x+vector[0], y+vector[1])
            
            if nx >=0 and ny >= 0 and nx < width and ny < height:
                c = lines[y][x]
                if c == 'E':
                    end = (x,y)
                    c = 'z'
                if c == 'S':
                    start = (x,y)
                    c = 'a'
                    
                if c == 'a':
                    lowest.add((x,y))

                c2 = lines[ny][nx]
                if c2 == 'E':
                    c2 = 'z'
                if c2 == 'S':
                    c2 = 'a'
                    
                d = ord(c2) - ord(c)
                
                if d <= 1:
                    paths[(nx, ny)].add((x,y))
                    
            vector = (-vector[1], vector[0])

def sd(q, paths, start):
    
    dist = {i: 9999 for i in q}
    dist[start] = 0
    
    while len(q) > 0:
        s = sorted(q.intersection(dist.keys()), key=lambda x: dist[x], reverse=True)
        
        u = s[-1]
        q.remove(u)
        
        for v in paths[u].intersection(q):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt

    return dist

dist = sd(q, paths, end)
            
print("Part 1:", dist[start])

print("Part 2:", min([x[1] for x in dist.items() if x[0] in lowest]))
