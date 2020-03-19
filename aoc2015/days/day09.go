package days

import (
	"errors"
	"fmt"
	"io"
	"os"
)

type Route struct {
	Dest string
	cost int
}

func Day09() {

	file, err := os.Open("input08.txt")
	if err != nil {
		return
	}
	defer file.Close()

	//reader := bufio.NewReader(file)

	for {
		//line, _, err := reader.ReadLine()

		if err == io.EOF {
			break
		}
	}

	routes := make(map[string]Route)

	totalcount := calc09(routes)

	fmt.Println("Part 1:", totalcount)
	//fmt.Println("Part 2:", doublequotecount-totalcount)

}

func calc09(routes map[string]Route) int {

	heldkarp(make(map[string]bool), routes, make([]string, 0))

	return 1

}

func pickrandom(passed map[string]bool, routes map[string]Route) (string, error) {
	for k := range routes {
		_, ok := passed[k]
		if !ok {
			return k, nil
		}

	}
	return "", errors.New("No choice")
}

func heldkarp(passedx map[string]bool, routes map[string]Route, path []string) []string {

	type ChoicesR struct {
		ontheroad map[string]bool
		end       string
	}

	// to dist
	//choices := make(map[ChoicesR]int)

	passed := make(map[string]bool)

	start, _ := pickrandom(passed, routes)
	passed[start] = true

	return []string{""}
}
