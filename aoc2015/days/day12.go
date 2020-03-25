package days

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
)

type filter = func(map[string]interface{}) bool

func Day12() {

	file, err := os.Open("input12.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	buf := make([]byte, 27277)

	readlen, err := reader.Read(buf)

	if err == io.EOF {
		return
	}

	var result map[string]interface{}
	jsonerr := json.Unmarshal(buf[0:readlen], &result)

	if jsonerr != nil {
		fmt.Println(jsonerr)
	}

	f1 := func(map[string]interface{}) bool {
		return true
	}

	sum1 := sum(result, f1)

	fmt.Println("Part 1:", sum1)

	f2 := func(m map[string]interface{}) bool {
		for _, v := range m {
			if parsed, ok := v.(string); ok {
				if parsed == "red" {
					return false
				}
			}
		}
		return true
	}

	sum2 := sum(result, f2)

	fmt.Println("Part 2:", sum2)
}

func sum(data map[string]interface{}, f filter) int {
	ret := 0

	if !f(data) {
		return 0
	}
	for _, v := range data {
		if parsed, ok := v.(map[string]interface{}); ok {
			ret += sum(parsed, f)
		} else if parsed, ok := v.([]interface{}); ok {
			ret += sumarray(parsed, f)
		} else {
			ret += sumsingle(v, f)
		}
	}

	return ret
}

func sumarray(data []interface{}, f filter) int {
	ret := 0
	for _, v := range data {
		ret += sumsingle(v, f)
	}
	return ret
}

func sumsingle(data interface{}, f filter) int {
	if parsed, ok := data.(float64); ok {
		return int(parsed)
	} else if parsed, ok := data.(map[string]interface{}); ok {
		return sum(parsed, f)
	} else if parsed, ok := data.([]interface{}); ok {
		return sumarray(parsed, f)
	}
	return 0
}
