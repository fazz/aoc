
text_file = open("input06.txt", "r")

input = [x.rstrip("\n\r") for x in text_file.readlines()][0]

def r(w):
    for i in range(0, len(input)-w+1):
        if len(set(input[i:i+w])) == w:
            break
    return i + w

print("Part 1:", r(4))
print("Part 1:", r(14))
