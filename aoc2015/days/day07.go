package days

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
)

type Rule struct {
	I1      string
	I2      string
	Operand func(uint16, uint16) uint16
}

var values map[string]uint16

func Day07() {

	file, err := os.Open("input07.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	rules := make(map[string]Rule)
	values = make(map[string]uint16)

	for {
		line, _, err := reader.ReadLine()

		sline := string(line)

		if err == io.EOF {
			break
		}

		// main form
		r1 := regexp.MustCompile(`^(?P<input>.+)\s->\s(?P<output>.+)`)
		substrings := r1.FindStringSubmatch(sline)
		output := substrings[2]

		// inputs
		r2 := regexp.MustCompile(`^(?P<i1>[a-z0-9]*?)\s{0,1}(?P<operand>NOT|RSHIFT|AND|LSHIFT|OR){0,1}\s{0,1}(?P<i2>[a-z0-9]+)$`)
		substrings2 := r2.FindStringSubmatch(substrings[1])

		paramsMap := make(map[string]string)
		for i, name := range r2.SubexpNames() {
			if i > 0 && i <= len(substrings2) {
				paramsMap[name] = substrings2[i]
			}
		}

		switch paramsMap["operand"] {
		case "NOT":
			rules[output] = Rule{"0", paramsMap["i2"], func(x, y uint16) uint16 {
				return ^y
			}}
		case "AND":
			rules[output] = Rule{paramsMap["i1"], paramsMap["i2"], func(x, y uint16) uint16 {
				return x & y
			}}
		case "OR":
			rules[output] = Rule{paramsMap["i1"], paramsMap["i2"], func(x, y uint16) uint16 {
				return x | y
			}}
		case "LSHIFT":
			rules[output] = Rule{paramsMap["i1"], paramsMap["i2"], func(x, y uint16) uint16 {
				return x << y
			}}
		case "RSHIFT":
			rules[output] = Rule{paramsMap["i1"], paramsMap["i2"], func(x, y uint16) uint16 {
				return x >> y
			}}
		default:
			rules[output] = Rule{"0", paramsMap["i2"], func(x, y uint16) uint16 {
				return y
			}}
		}

	}

	result1 := calc07("a", rules)

	fmt.Println("Part 1:", result1)

	values = make(map[string]uint16)
	rules["b"] = Rule{"0", "0", func(x, y uint16) uint16 {
		return result1
	}}

	result2 := calc07("a", rules)

	fmt.Println("Part 2:", result2)

}

func calc07(tocalc string, rules map[string]Rule) uint16 {

	cached, found := values[tocalc]
	if found {
		return cached
	}

	r := rules[tocalc]

	var i1, i2 uint16

	i1_64, err := strconv.ParseUint(r.I1, 10, 16)

	if err != nil {
		i1 = calc07(r.I1, rules)
	} else {
		i1 = uint16(i1_64)
	}

	i2_64, err := strconv.ParseUint(r.I2, 10, 16)

	if err != nil {
		i2 = calc07(r.I2, rules)
	} else {
		i2 = uint16(i2_64)
	}

	ret := r.Operand(i1, i2)
	values[tocalc] = ret
	return ret

}
