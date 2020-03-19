package days

import (
	"fmt"
	"strconv"
)

func Day10() {

	input := "1113122113"

	sum := sumup(input, 40)

	fmt.Println("Part 1:", sum)

	sum = sumup(input, 50)
	fmt.Println("Part 2:", sum)

}

func sumup(input string, count int) int {
	if count == 0 {
		return len(input)
	}
	v := calc10(input)
	splits := splitup(v)

	sum := 0
	for i := range splits {
		sum += sumup(splits[i], count-1)
	}
	return sum

}

func splitup(input string) []string {
	output := make([]string, 0)
	l := len(input)
	last := 0
	skip := 0
	for i, c := range input {
		if skip > 0 {
			skip--
			continue
		}

		// This is one particular independent splitting point, good
		// enough for optimization.
		if c == '2' && i < l-3 {
			if input[i+1] == '1' && input[i+2] == '3' && input[i+3] == '2' {
				output = append(output, input[last:i+1])
				last = i + 1
				skip = 2
			}
		}
	}
	output = append(output, input[last:])
	return output
}

func calc10(input string) string {
	count := 0
	var pc rune
	output := ""
	pc = 'x'

	for _, c := range input {
		if pc == 'x' {
			pc = c
		}
		if c == pc {
			count++
		} else {
			output = output + strconv.Itoa(count)
			output = output + string(pc)
			count = 1
			pc = c
		}
	}
	output = output + strconv.Itoa(count)
	output = output + string(pc)
	return output
}
