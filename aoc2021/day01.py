
text_file = open("input01.txt", "r")

prev = None
count = 0

numbers = list(map(int, [x.rstrip("\n\r") for x in text_file.readlines()]))

count = sum(1 for x in filter(lambda x: x > 0, [(numbers[i+1] - numbers[i]) for i in range(len(numbers)-1)]))

print("Part1: ", count)

count = sum(1 for x in filter(lambda x: x > 0, [(numbers[i+3] - numbers[i]) for i in range(len(numbers)-3)]))

print("Part2: ", count)
