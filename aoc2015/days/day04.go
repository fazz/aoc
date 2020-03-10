package days

import (
	"crypto/md5"
	"fmt"
	"strconv"
)

func Day04() {

	input := "iwrupvqb"

	var min1 int64 = 0
	var min2 int64 = 0
	var i int64
	for i = 0; i >= 0; i++ {
		str := input + strconv.FormatInt(i, 10)

		value := md5.Sum([]byte(str))

		if value[0] == 0 && value[1] == 0 && value[2] <= 15 {
			if min1 == 0 {
				min1 = i
			}
			if value[2] == 0 {
				min2 = i
				break
			}
		}
	}

	fmt.Println("Part 1:", min1)
	fmt.Println("Part 2:", min2)

}
