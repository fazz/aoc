package days

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

var totalcount int64
var meaningfulcount int64
var doublequotecount int64

func Day08() {

	file, err := os.Open("input08.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	for {
		line, _, err := reader.ReadLine()

		if err == io.EOF {
			break
		}

		doublequotecount += 2 // new quotes around it

		for i := 0; i < len(line); i++ {
			c := line[i]
			totalcount++

			if c == '"' {
				doublequotecount += 2
				continue // simple doublequote, start or end
			} else if c == '\\' {
				if line[i+1] == 'x' {
					i += 3
					totalcount += 3
					meaningfulcount += 1
					doublequotecount += 5
				} else {
					i += 1
					totalcount += 1
					meaningfulcount += 1
					doublequotecount += 4
				}

			} else {
				meaningfulcount++
				doublequotecount++
			}

		}
	}

	fmt.Println("Part 1:", totalcount-meaningfulcount)
	fmt.Println("Part 2:", doublequotecount-totalcount)

}
