#from functools import filter
import re

text_file = open("input19.txt", "r")

lines = [x.rstrip("\n\r") for x in text_file.readlines()]

def serbyarr(rule, rules, sbi):
    if isinstance(rule[0], str):
        return rule[0]
   
    return "".join([sbi(r, rules, sbi) for r in rule])

def serbyint1(ruleno, rules, sbi):
    rule = rules[ruleno]

    (a, b) = ("(", ")") if len(rule) > 1 else ("", "")
    return a + "|".join([serbyarr(rulearr, rules, sbi) for rulearr in rule]) + b

def serbyint2(ruleno, rules, sbi):
    if ruleno == 8:
        return "(" + serbyint1(ruleno, rules, serbyint1) + ")+"

    if ruleno == 11:
        s42 = [serbyint1(42, rules, serbyint1) for rulearr in rules[ruleno]][0]
        s31 = [serbyint1(31, rules, serbyint1) for rulearr in rules[ruleno]][0]
        return "(" + "|".join([s42*x + s31*x for x in range(1, 5)]) + ")"

    return serbyint1(ruleno, rules, sbi)

def calc(lines, part2):
    ruleread = True
    result = 0
    rules = {}
    re0 = ""
    for l in lines:
        if len(l) == 0:
            re0 = re.compile("^" + serbyint1(0, rules, serbyint2 if part2 else serbyint1) + "$")
            ruleread = False

        if ruleread:
            (idx, rule) = map(lambda s: s.lstrip(), l.split(':'))
            idx = int(idx)

            if rule[0] == '"':
                rules[idx] = rule[1]
            else:
                alt = map(lambda a: a.strip(), rule.split(' | '))
                rules[idx] = [tuple(map(int, a.split(' '))) for a in alt]
        else:
            result += 1 if re0.match(l) is not None else 0
    return result

print("Part1:", calc(lines, False))
print("Part2:", calc(lines, True))

#
#
#

def expand(idx, rules, part2):
    ret = ""
    for c in rules[idx]:
        if isinstance(c, str):
            ret += c
        else:
            if part2 and c == 8:
                ret += "(" + expand(8, rules, False) + ")+"
            elif part2 and c == 11:
                s42 = expand(42, rules, False)
                s31 = expand(31, rules, False)
                ret += "(" + "|".join([s42*x + s31*x for x in range(1, 5)]) + ")"
            else:
                ret += expand(c, rules, part2)
    return ret

def calc2(lines, part2):
    rules = {}
    s = lines.index("")
    for l in lines[0:s]:
        (idx, rule) = map(lambda s: s.lstrip().replace('"', ''), l.split(':'))
        rules[int(idx)] = (['('] if '|' in rule else []) + [(lambda z: int(z) if z.isdecimal() else z)(x) for x in rule.split(' ')] + ([')'] if '|' in rule else [])

    re0 = re.compile("^" + expand(0, rules, part2) + "$")
    return len(list(filter(lambda x: re0.match(x) is not None, (l for l in lines[s+1:]))))

print("Part1:", calc2(lines, False))
print("Part2:", calc2(lines, True))
