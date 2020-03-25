package days

import (
	"aoc2015/common"
	"fmt"
	"regexp"
)

func Day11() {

	pwcandidate := addtostring("vzbxkghb", 1)

	//

	re1 := "(abc"

	p1 := "bcd"

	for p1[2] != 'a' {
		re1 += "|"
		re1 += p1
		p1 = addtostring(p1, 111)
	}

	re1 += ")"

	r1 := regexp.MustCompile(re1)

	//

	r2 := regexp.MustCompile("(i|o|l)")

	//

	re3 := "(aa"

	p3 := "bb"

	for p3[1] != 'a' {
		re3 += "|"
		re3 += p3

		p3 = addtostring(p3, 11)
	}

	re3 += ")"

	re3 = re3 + ".*" + re3

	r3 := regexp.MustCompile(re3)

	f := func(pw string) string {
		for true {

			match1 := r1.FindStringSubmatch(pw)
			match2 := r2.FindStringSubmatch(pw)
			match3 := r3.FindStringSubmatch(pw)

			if len(match1) > 0 && len(match2) == 0 && len(match3) > 0 {
				break
			}

			pw = addtostring(pw, 1)
		}
		return pw
	}

	pwcandidate = f(pwcandidate)
	fmt.Println("Part 1:", pwcandidate)

	pwcandidate = f(addtostring(pwcandidate, 1))
	fmt.Println("Part 2:", pwcandidate)
}

func addtostring(input string, add int) string {

	res := ""
	carry := byte(0)

	for i := len(input) - 1; i >= 0; i-- {
		a := (add / common.IPow(10, int(len(input)-i-1))) % 10

		c := input[i] + byte(a) + carry
		if c > 'z' {
			c = 'a'
			carry = 1
		} else {
			carry = 0
		}

		res = string(c) + res
	}

	return res
}
