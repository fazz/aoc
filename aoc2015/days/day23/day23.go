package day23

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
)

func Exec() {

	file, err := os.Open("input23.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	type Opcode struct {
		name string
		op1r string
		op1o int64
		op2o int64
	}

	opcodes := make([]Opcode, 0)

	for {
		line, _, err := reader.ReadLine()

		sline := string(line)

		if err == io.EOF {
			break
		}
		r := regexp.MustCompile(`^(?P<command>(hlf|tpl|inc|jmp|jie|jio))\s(?P<OP1>(a|b|\+|-|[0-9]){0,10})(,\s(?P<OP2>(\+|-|[0-9]){0,10})){0,1}`)
		match := r.FindStringSubmatch(sline)

		paramsMap := make(map[string]string)
		for i, name := range r.SubexpNames() {
			if i > 0 && i <= len(match) {
				paramsMap[name] = match[i]
			}
		}

		offset1, _ := strconv.ParseInt(paramsMap["OP1"], 10, 64)
		offset2, _ := strconv.ParseInt(paramsMap["OP2"], 10, 64)

		opcode := Opcode{
			paramsMap["command"],
			paramsMap["OP1"],
			offset1,
			offset2,
		}

		opcodes = append(opcodes, opcode)
	}

	calc := func(a, b int) int {
		registers := make(map[string]int)
		registers["a"] = a
		registers["b"] = b

		pc := (int64)(0)
		for pc < (int64)(len(opcodes)) {

			register := opcodes[pc].op1r

			switch opcodes[pc].name {
			case "hlf":
				registers[register] /= 2
				pc++
			case "tpl":
				registers[register] *= 3
				pc++
			case "inc":
				registers[register]++
				pc++
			case "jmp":
				pc += opcodes[pc].op1o
			case "jie":
				if registers[register]%2 == 0 {
					pc += opcodes[pc].op2o
				} else {
					pc++
				}
			case "jio":
				if registers[register] == 1 {
					pc += opcodes[pc].op2o
				} else {
					pc++
				}
			}
		}
		return registers["b"]
	}

	fmt.Println("Part 1:", calc(0, 0))
	fmt.Println("Part 2:", calc(1, 0))
}
