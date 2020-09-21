package day22

import (
	"aoc2015/common"
	"container/heap"
	"fmt"
)

type spell struct {
	Name                                          string
	Cost, Damage, Heal, Armor, Recharge, Duration int
}

type gameState struct {
	Number         int
	ManaCost       int
	ManaLeft       int     // @ end of the turn
	PointsLeft     int     // @ end of the turn
	BossPointsLeft int     // @ end of the turn
	ActiveSpells   []spell // @ end of the turn
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*gameState

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].ManaCost < pq[j].ManaCost
}

func (pq *PriorityQueue) Push(x interface{}) {
	item := x.(*gameState)
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil // avoid memory leak
	*pq = old[0 : n-1]
	return item
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func newGameState(cgs gameState) (gameState, int) {

	newgs := cgs
	newgs.ActiveSpells = make([]spell, 0)

	var activeArmour int
	for i := range cgs.ActiveSpells {
		as := cgs.ActiveSpells[i]

		newgs.PointsLeft += as.Heal
		activeArmour += as.Armor
		newgs.BossPointsLeft -= as.Damage
		newgs.ManaLeft += as.Recharge
		as.Duration--
		if as.Duration >= 1 {
			newgs.ActiveSpells = append(newgs.ActiveSpells, as)
		}
	}
	return newgs, activeArmour
}

func Exec() {

	Spells := []spell{
		{"Magic Missile", 53, 4, 0, 0, 0, 1},
		{"Drain", 73, 2, 2, 0, 0, 1},
		{"Shield", 113, 0, 0, 7, 0, 6},
		{"Poison", 173, 3, 0, 0, 0, 6},
		{"Recharge", 229, 0, 0, 0, 101, 5},
	}

	BossPoints := 71
	BossDamage := 10

	PlayerPoints := 50
	PlayerMana := 500

	play := func(penalty int) int {

		pq := make(PriorityQueue, 0)
		heap.Init(&pq)

		{
			// Init game, player's first move
			gs := &gameState{
				0, 0, PlayerMana, PlayerPoints, BossPoints, []spell{},
			}

			heap.Push(&pq, gs)
		}

		visited := make(map[string]bool)

		// Go looking for the most optimal move
		for pq.Len() > 0 {
			gs := heap.Pop(&pq).(*gameState)

			visited[fmt.Sprintf("%v", *gs)] = true

			if gs.Number%2 == 0 {
				// Player move

				if gs.PointsLeft-penalty <= 0 {
					continue
				}

				// Look up next potential spells.
				for i := range Spells {
					s := Spells[i]

					newgs, _ := newGameState(*gs)
					newgs.Number++
					newgs.PointsLeft -= penalty

					if newgs.ManaLeft-s.Cost < 0 {
						continue
					}
					active := false
					for i := range newgs.ActiveSpells {
						if newgs.ActiveSpells[i].Name == s.Name {
							active = true
						}
					}
					if active {
						continue
					}

					newgs.ActiveSpells = append(newgs.ActiveSpells, s)

					if newgs.BossPointsLeft <= 0 {
						return newgs.ManaCost
					}

					newgs.ManaCost += s.Cost
					newgs.ManaLeft -= s.Cost

					if _, ok := visited[fmt.Sprintf("%v", newgs)]; !ok {
						heap.Push(&pq, &newgs)
					}

				}
			} else {
				// Boss move

				newgs, activeArmour := newGameState(*gs)
				newgs.Number++

				// Damage to boss
				if newgs.BossPointsLeft <= 0 {
					// Player wins
					return newgs.ManaCost
				}

				// Boss hits
				newgs.PointsLeft -= common.IMax(1, BossDamage-activeArmour)
				if newgs.PointsLeft > 0 {
					if _, ok := visited[fmt.Sprintf("%v", newgs)]; !ok {
						heap.Push(&pq, &newgs)
					}
				} else {
					// Player is dead, go looking for other options
				}
			}
		}
		return 0
	}

	result1 := play(0)
	result2 := play(1)

	fmt.Println("Part 1:", result1)
	fmt.Println("Part 2:", result2)
}
