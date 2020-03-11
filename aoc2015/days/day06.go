package days

import (
	"aoc2015/common"
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
)

func Day06() {

	file, err := os.Open("input06.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	lights1 := make([]int8, 1000000)
	lights2 := make([]int8, 1000000)

	for {
		line, _, err := reader.ReadLine()

		sline := string(line)

		if err == io.EOF {
			break
		}
		r := regexp.MustCompile(`^(?P<command>(turn off|turn on|toggle))\s(?P<X1>\d{1,3}),(?P<Y1>\d{1,3})\sthrough\s(?P<X2>\d{1,3}),(?P<Y2>\d{1,3})`)
		match := r.FindStringSubmatch(sline)

		paramsMap := make(map[string]string)
		for i, name := range r.SubexpNames() {
			if i > 0 && i <= len(match) {
				paramsMap[name] = match[i]
			}
		}

		X1, _ := strconv.ParseUint(paramsMap["X1"], 10, 32)
		Y1, _ := strconv.ParseUint(paramsMap["Y1"], 10, 32)
		X2, _ := strconv.ParseUint(paramsMap["X2"], 10, 32)
		Y2, _ := strconv.ParseUint(paramsMap["Y2"], 10, 32)

		X1, X2 = common.USwap64(X1, X2)
		Y1, Y2 = common.USwap64(Y1, Y2)

		for x := X1; x <= X2; x++ {
			for y := Y1; y <= Y2; y++ {
				i := 1000*x + y
				switch paramsMap["command"] {
				case "turn off":
					lights1[i] = 0
					lights2[i] = common.I8Max(lights2[i]-1, 0)
				case "turn on":
					lights1[i] = 1
					lights2[i]++
				case "toggle":
					lights1[i] = lights1[i] ^ 1
					lights2[i] = lights2[i] + 2
				}

			}
		}
	}

	lit := common.I8Filter(lights1, func(v int8) bool {
		return v == 1
	})

	count1 := len(lit)

	fmt.Println(lights2)
	count2 := common.I8LFold(lights2, 0, func(v int8, s int64) int64 {
		return s + int64(v)
	})

	fmt.Println("Part 1:", count1)
	fmt.Println("Part 2:", count2)

}
