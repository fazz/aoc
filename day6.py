
text_file = open("input6.txt", "r")
lines = text_file.readlines()

pairs = list(map(lambda x: tuple(x.strip().split(')')), lines))

orbiting = {}
parents = {}

for p in pairs:
    orbiting.setdefault(p[0], set()).add(p[1])
    parents[p[1]] = p[0]

print(orbiting)

def calc(start, depth):
    res = 0
    for b in orbiting.get(start, []):
        res += 1 + depth
        res += calc(b, depth+1)

    return res

#print(calc('COM', 0))

tracks = {}

for body in ['YOU', 'SAN']:
    p = parents[body]
    while p != 'COM':
        tracks.setdefault(body, []).append(p)
        p = parents[p]

while tracks['YOU'][-1:] == tracks['SAN'][-1:]:
    del tracks['YOU'][-1]
    del tracks['SAN'][-1]

print(len(tracks['YOU']) + len(tracks['SAN']))

