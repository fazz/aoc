import re

text_file = open("input04.txt", "r")
lines = text_file.readlines()

def count(lines, validator):
    fields = {}
    result = 0

    for l in lines:
        l = l[:-1]
        if len(l) == 0:
            rfields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
            c = 0
            for rf in rfields:
                if rf in fields and validator(rf, fields[rf]):
                    c += 1
            if c == len(rfields):
                result += 1

            fields = {}
        else:
            ls = l.split(' ')
            for ll in ls:
                (f, v) = ll.split(':')
                fields[f] = v
    return result

def blank(f, v):
    return True

rrhgt = re.compile("^([0-9].+)(in|cm)$")
rrhcl = re.compile("^\#[0-9a-f]{6}$")
rrpid = re.compile("^[0-9]{9}$")

def validator(f, v):
    if f == "byr":
        return 1920 <= int(v) <= 2002
    elif f == "iyr":
        return 2010 <= int(v) <= 2020
    elif f == "eyr":
        return 2020 <= int(v) <= 2030
    elif f == "hgt":
        m = rrhgt.match(v)
        if m:
            v = int(m.group(1))
            if m.group(2) == "in":
                return 59 <= v <= 76
            else:
                return 150 <= v <= 193
        return False
    elif f == "hcl":
        return rrhcl.match(v) is not None
    elif f == "ecl":
        return v in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    elif f == "pid":
        return rrpid.match(v) is not None
    return True


print("Part1:", count(lines, blank))
print("Part2:", count(lines, validator))
