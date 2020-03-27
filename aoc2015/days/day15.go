package days

import (
	"aoc2015/common"
	"fmt"
	"strconv"
)

func Day15() {

	type Ing struct {
		a []int
	}

	type path struct {
		ings  map[string]int
		amts  []int
		score int
	}
	// len -> ingredient set -> amt [5]int
	paths := make(map[int]map[string]path)

	add := func(i map[string]Ing, n string, p1, p2, p3, p4, p5 int) map[string]Ing {
		i[n] = Ing{a: []int{p1, p2, p3, p4, p5}}

		return i
	}

	ing := make(map[string]Ing)

	ing = add(ing, "Sprinkles", 5, -1, 0, 0, 5)
	ing = add(ing, "PeanutButter", -1, 3, 0, 0, 1)
	ing = add(ing, "Frosting", 0, -1, 4, 0, 6)
	ing = add(ing, "Sugar", -1, 0, 0, 2, 8)

	stableing := make([]string, 0)
	for k := range ing {
		stableing = append(stableing, k)
	}

	normalize := func(ing map[string]int) string {
		ret := ""
		for _, v := range stableing {
			ret += v
			ret += strconv.FormatInt(int64(ing[v]), 16)
		}
		return ret
	}

	calc := func(amt []int, extra string) (int, []int) {
		ret := 1

		retamts := append([]int(nil), amt...)

		ve, oke := ing[extra]
		for i := 0; i < 5; i++ {
			if oke {
				retamts[i] += ve.a[i]
			}
			if i != 4 {
				retamts[i] = common.IMax(0, retamts[i])
				ret *= retamts[i]
			}
		}
		return ret, retamts
	}

	{
		amt := []int{0, 0, 0, 0, 0}

		ingnames := make(map[string]int)

		for k, v := range ing {
			for i := 0; i < 5; i++ {
				amt[i] += v.a[i]
			}
			ingnames[k] = 1
		}
		score, _ := calc(amt, "")

		paths[4] = map[string]path{normalize(ingnames): path{ingnames, amt, score}}
	}

	for pathlen := 4; pathlen < 100; pathlen++ {

		fmt.Println(pathlen, len(paths[pathlen]))

		paths[pathlen+1] = make(map[string]path)

		for _, v := range paths[pathlen] {
			for iname := range ing {

				newings := make(map[string]int)
				for k := range v.ings {
					newings[k] = v.ings[k]
				}
				newings[iname]++

				newkey := normalize(newings)

				if _, ok := paths[pathlen+1][newkey]; ok {
					continue
				}

				newscore, newamts := calc(v.amts, iname)

				if newscore <= 0 {
					continue
				}

				paths[pathlen+1][newkey] = path{newings, newamts, newscore}
			}
		}
	}

	fmt.Println(len(paths[100]))

	score1 := 0
	for _, v := range paths[100] {
		score1 = common.IMax(score1, v.score)
	}

	fmt.Println("Part 1:", score1)

	maxcal := 0

	score2 := 0

	for _, v := range paths[100] {

		maxcal = common.IMax(maxcal, v.amts[4])

		if v.amts[4] == 500 {
			score2 = common.IMax(score2, v.score)
		}

	}

	fmt.Println("Part 2:", score2)
}
