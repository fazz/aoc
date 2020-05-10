package day21

import (
	"aoc2015/common"
	"fmt"
	"math"
)

func divCeil(a, b int) int {
	r := a / b
	if a%b != 0 {
		r++
	}
	return r
}

func Exec() {

	BossPoints := 109
	BossArmor := 2
	BossDamage := 8

	PlayerPoints := 100

	Weapons := map[int]int{4: 8, 5: 10, 6: 25, 7: 40, 8: 74}
	Armors := map[int]int{0: 0, 1: 13, 2: 31, 3: 53, 4: 75, 5: 102}

	type Ring struct {
		D, A, C int
	}

	Rings := []Ring{{0, 0, 0}, {1, 0, 25}, {2, 0, 50}, {3, 0, 100}, {0, 1, 20}, {0, 2, 40}, {0, 3, 80}}

	MaxPlayerDamage := 13
	MinPlayerDamage := 4

	// armor - damage - cost
	MinCosts := make(map[int]map[int]int)
	MaxCosts := make(map[int]map[int]int)

	for ak, av := range Armors {
		for dk, dv := range Weapons {
			for r1i, r1v := range Rings {
				for r2i, r2v := range Rings {
					if r1i == r2i {
						continue
					}
					a := ak + r1v.A + r2v.A
					d := dk + r1v.D + r2v.D
					c := av + dv + r1v.C + r2v.C
					if _, ok := MinCosts[a]; !ok {
						MinCosts[a] = make(map[int]int)
					}
					if _, ok := MaxCosts[a]; !ok {
						MaxCosts[a] = make(map[int]int)
					}
					if _, ok := MinCosts[a][d]; !ok {
						MinCosts[a][d] = c
					} else {
						MinCosts[a][d] = common.IMin(MinCosts[a][d], c)
					}
					if _, ok := MaxCosts[a][d]; !ok {
						MaxCosts[a][d] = c
					} else {
						MaxCosts[a][d] = common.IMax(MaxCosts[a][d], c)
					}
				}
			}
		}
	}

	result1 := math.MaxInt32
	result2 := 0

	for i := BossDamage; i >= 1; i-- {
		hitsBoss := divCeil(PlayerPoints, i)

		for j := MinPlayerDamage - BossArmor; j <= MaxPlayerDamage-BossArmor; j++ {
			hitsPlayer := divCeil(BossPoints, j)
			playerArmor := common.IMin(7, BossDamage-i)
			playerDamage := j + BossArmor
			fmt.Println(playerArmor, playerDamage)

			if hitsPlayer > hitsBoss {
				if c, ok := MaxCosts[playerArmor][playerDamage]; ok {
					result2 = common.IMax(result2, c)
					// 171 too low
				}
			} else {
				if c, ok := MinCosts[playerArmor][playerDamage]; ok {
					result1 = common.IMin(result1, c)
				}
			}
		}
	}

	fmt.Println("Part 1:", result1)
	fmt.Println("Part 2:", result2)
}
