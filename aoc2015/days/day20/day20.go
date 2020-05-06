package day20

import (
	"fmt"
)

func pf(i int) int {
	return ((3 * i * i) - i) / 2
}

func sigma(input int) int {

	result := 0

	for i := 1; true; i++ {
		sign := 1
		if i&1 == 0 {
			sign = -1
		}

		{
			is1 := input - pf(i)

			s1 := input
			if is1 < 0 {
				return result
			} else if is1 != 0 {
				s1 = sigmaCached(is1)
			}

			result += sign * s1
		}

		{
			is2 := input - pf(-i)

			s2 := input
			if is2 < 0 {
				return result
			} else if is2 != 0 {
				s2 = sigmaCached(is2)
			}

			result += sign * s2
		}
	}

	return result
}

var sigmacache = make(map[int]int)

func sigmaCached(i int) int {

	if v, ok := sigmacache[i]; ok {
		return v
	}
	v2 := sigma(i)
	sigmacache[i] = v2
	return v2
}

func Exec() {

	INPUT := 34000000

	result1 := INPUT / 50
	for ; ; result1++ {
		v := sigmaCached(result1)
		if v >= INPUT/10 {
			break
		}
	}

	fmt.Println("Part 1:", result1)

	result2 := INPUT / 41

	for ; ; result2++ {
		v := 0

		for i := result2; i >= 1; i-- {
			if result2%i == 0 {
				if result2/i <= 50 {
					v += i
				} else {
					break
				}
			}
		}
		if v*11 >= INPUT {
			break
		}
	}

	fmt.Println("Part 2:", result2)
}
