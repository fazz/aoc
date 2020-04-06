package days

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func Day18() {

	load := func() map[int]map[int]int {
		file, err := os.Open("input18.txt")
		if err != nil {
			return nil
		}
		defer file.Close()

		reader := bufio.NewReader(file)

		lights := make(map[int]map[int]int)

		for i := 0; true; i++ {
			line, _, err := reader.ReadLine()

			if err == io.EOF {
				break
			}

			lights[i] = make(map[int]int)

			for j, c := range line {
				switch c {
				case '#':
					lights[i][j] = 1
				case '.':
					lights[i][j] = 0
				}
			}
		}
		return lights
	}

	nbcount := func(cycle, x, y int, lights map[int]map[int]int) int {
		cycle = cycle & 1

		result := 0

		for i := -1; i <= 1; i++ {
			for j := -1; j <= 1; j++ {
				if i == 0 && j == 0 {
					continue
				}
				x1 := x + i
				y1 := y + j
				result += (lights[x1][y1] >> cycle) & 1
			}
		}
		return result
	}

	CYCLES := 100
	DIM := 100

	calc := func(lights map[int]map[int]int, corners bool) int {

		for cycle := 0; cycle < CYCLES; cycle++ {
			for i := 0; i < DIM; i++ {
				for j := 0; j < DIM; j++ {

					nc := nbcount(cycle, i, j, lights)

					light := (lights[i][j] >> (cycle % 2)) & 1

					if nc == 3 || (light > 0 && (nc == 2)) {
						lights[i][j] |= 1 << ((cycle + 1) & 1)
					} else {
						lights[i][j] &= 1 << (cycle & 1)
					}
				}
			}

			if corners {
				lights[0][DIM-1] = 3
				lights[DIM-1][DIM-1] = 3
				lights[DIM-1][0] = 3
				lights[0][0] = 3
			}
		}

		count := 0

		for i := 0; i < DIM; i++ {
			for j := 0; j < DIM; j++ {
				count += (lights[i][j] >> (CYCLES & 1)) & 1
			}
		}
		return count
	}

	lights := load()

	fmt.Println("Part 1:", calc(lights, false))

	lights = load()

	fmt.Println("Part 2:", calc(lights, true))
}
