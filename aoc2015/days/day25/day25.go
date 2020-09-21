package day25

import (
	"fmt"
	"math/big"
)

func Exec() {

	calc := func() int64 {
		row := (int64)(2947)
		col := (int64)(3029)

		realrow := row + col - 2

		n := (realrow*realrow + realrow + 2) / 2

		pos := n + col - 1

		fmt.Println(pos)

		mod := big.NewInt(33554393)
		multiplier := big.NewInt(252533)
		multiplier = multiplier.Exp(multiplier, big.NewInt((int64)(pos-1)), mod)

		result := big.NewInt(20151125)
		result.Mul(result, multiplier)
		result.Mod(result, mod)

		return result.Int64()
	}

	fmt.Println("Part 1:", calc())

	//	N := big.NewInt((int64)(n))

	//	fposition := (Int.Exp(n, 2) + n + 2) / 2

	//fmt.Println("Part 1:", result1)
	//fmt.Println("Part 2:", result2)
}
