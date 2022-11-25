
text_file = open("input02.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

result1 = 0

for l in lines:
    li = [int(x) for x in l.split('\t')]
    result1 += abs(min(li)-max(li))

print("Part 1", result1)

result2 = 0

for l in lines:
    li = sorted([int(x) for x in l.split('\t')], reverse=True)
    
    for i in range(len(li)-1):
        for j in range(i+1, len(li)):
            if li[i]//li[j]*li[j] == li[i]:
                result2 += li[i]//li[j]

print("Part 2", result2)
