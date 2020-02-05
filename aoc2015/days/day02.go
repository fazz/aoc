package days

import ("fmt"
		"bufio"
		"io"
		"os"
		"strings"
		"strconv"
		"aoc2015/common"
)

func Day02() {

	file, err := os.Open("input02.txt")
	if err != nil {
        return
    }
	defer file.Close()
	
	reader := bufio.NewReader(file)

	var sum int64 = 0
	var ribbon int64 = 0

	for {
		line, _, err := reader.ReadLine()

		if err == io.EOF {
				break
		}

		numberss := strings.Split(string(line), "x")

		var n []int64
		var ssum int64 = 0

		for i := range numberss {
			v, _ := strconv.ParseInt(numberss[i], 10, 64)
			n = append(n, v)
		}

		var ms int64 = 100000000000
		var mc int64 = 100000000000

		for i := 0; i <= 2; i++ {
			for j := i+1; j <= 2; j++ {
				side := n[i]*n[j]
				ms = common.Min(side, ms)
				mc = common.Min(2*n[i]+2*n[j], mc)
				ssum += 2*side
			}
		}

		sum += ssum + ms
		ribbon += mc + (n[0]*n[1]*n[2])
	}

	fmt.Println("Part 1:", sum)
 	fmt.Println("Part 2:", ribbon)


}


