package days

import (
	"aoc2015/common"
	"fmt"
)

type day14R struct {
	Speed int
	STime int
	RTime int
	CTime int
	CDist int
}

func day14add(i map[string]day14R, n string, s, st, rt int) map[string]day14R {

	i[n] = day14R{Speed: s, STime: st, RTime: rt, CTime: st + rt, CDist: s * st}

	return i

}

func Day14() {

	reindeers := make(map[string]day14R)

	reindeers = day14add(reindeers, "Vixen", 8, 8, 53)
	reindeers = day14add(reindeers, "Blitzen", 13, 4, 49)
	reindeers = day14add(reindeers, "Rudolph", 20, 7, 132)
	reindeers = day14add(reindeers, "Cupid", 12, 4, 43)
	reindeers = day14add(reindeers, "Donner", 9, 5, 38)
	reindeers = day14add(reindeers, "Dasher", 10, 4, 37)
	reindeers = day14add(reindeers, "Comet", 3, 37, 76)
	reindeers = day14add(reindeers, "Prancer", 9, 12, 97)
	reindeers = day14add(reindeers, "Dancer", 37, 1, 36)

	TIME := 2503

	_, p1 := calc14(TIME, reindeers)

	fmt.Println("Part 1:", p1)

	points := make(map[string]int)

	for i := 1; i <= TIME; i++ {
		names, _ := calc14(i, reindeers)

		for _, name := range names {

			if _, ok := points[name]; !ok {
				points[name] = 0
			}

			points[name] = points[name] + 1
		}
	}

	p2 := 0
	for _, v := range points {
		p2 = common.IMax(p2, v)
	}

	fmt.Println("Part 2:", p2)
}

func calc14(time int, reindeers map[string]day14R) ([]string, int) {

	max := 0
	maxnames := make([]string, 0)

	for k, v := range reindeers {

		dist := 0

		cycles := time / v.CTime

		dist += cycles * v.CDist

		timeleftmoving := common.IMin(time%v.CTime, v.STime)

		dist += timeleftmoving * v.Speed

		if dist >= max {
			if dist == max {
				maxnames = append(maxnames, k)
			} else {
				maxnames = []string{k}
			}
			max = dist
		}
	}
	return maxnames, max
}
