package days

import (
	"aoc2015/common"
	"fmt"
	"math"
)

func Day17() {

	bottles_ := []int{
		50,
		44,
		11,
		49,
		42,
		46,
		18,
		32,
		26,
		40,
		21,
		7,
		18,
		43,
		10,
		47,
		36,
		24,
		22,
		40,
	}

	TOTAL := int(150)

	bottles := make(map[int]int)

	for i, v := range bottles_ {
		bottles[int(i)] = v
	}

	bycount := make(map[int]int)

	result := calc17(0, TOTAL, 0, bottles, bycount)

	fmt.Println("Part 1:", result)

	part2idx := math.MaxInt32
	for k := range bycount {
		part2idx = common.IMin(k, part2idx)
	}

	fmt.Println("Part 2:", bycount[part2idx])
}

func calc17(start, limit, bottlecount int, bottles, bycount map[int]int) int {
	result := 0

	if start >= len(bottles) {
		return 0
	}

	// Do not take start
	result += calc17(start+1, limit, bottlecount, bottles, bycount)

	// Take start
	limit -= bottles[start]
	if limit == 0 {
		result++
		if _, ok := bycount[bottlecount+1]; !ok {
			bycount[bottlecount+1] = 0
		}
		bycount[bottlecount+1]++
	} else if limit > 0 {
		result += calc17(start+1, limit, bottlecount+1, bottles, bycount)
	}

	return result
}
