
from aocd import data, post

ll = len(data)

result1 = 0

for i in range(ll):
    if data[i] == data[(i+1)%ll]:
        result1 += int(data[i])

post.submit(result1, part="a", day=1, year=2017)

result2 = 0

for i in range(ll):
    if data[i] == data[(i+ll//2)%ll]:
        result2 += int(data[i])

post.submit(result2, part="b", day=1, year=2017)

