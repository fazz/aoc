from copy import deepcopy
from functools import reduce
import operator
from collections import defaultdict

lines = [x.rstrip("\n\r").lstrip(' ') for x in open("input11.txt", "r")]

monkeys = []
checks = set()

for li in range((len(lines)+1)//7):
    l = lines[li*7:li*7+7]
    
    items = [int(x.rstrip(',')) for x in l[1].split(' ')[2:]]
              
    operand = l[2].split(' ')[5]
    
    op1 = operator.add if l[2].split(' ')[4] == '+' else operator.mul
    
    if operand == 'old':
        op2 = lambda op,x,_: op(x,x)
    else:
        op2 = lambda op,x,y: op(x,y)
        operand = int(l[2].split(' ')[5])
        
    test = int(l[3].split(' ')[3])
    checks.add(test)
    
    truetarget = int(l[4].split(' ')[5])
    falsetarget = int(l[5].split(' ')[5])
    
    monkeys.append( (items, op1, op2, operand, test, truetarget, falsetarget) )
    
group = reduce(operator.mul, checks, 1)    

def calc(monkeys, rounds, reducer):
    activity = defaultdict(int)
    for _ in range(rounds):
        for m in range(len(monkeys)):
            while len(monkeys[m][0]) > 0:
                activity[m] += 1
                item = monkeys[m][0].pop(0)

                item = monkeys[m][2](monkeys[m][1], item, monkeys[m][3])

                item = reducer(item)

                if item % monkeys[m][4] == 0:
                    target = monkeys[m][5]
                else:
                    target = monkeys[m][6]
                monkeys[target][0].append(item)
            
    r = sorted(activity.values(), reverse=True)[0:2]
    return operator.mul(*r)

print("Part 1:", calc(deepcopy(monkeys), 20, lambda x: x // 3))
print("Part 2:", calc(monkeys, 10000, lambda x: x % group))
