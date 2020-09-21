package day24

import (
	"bufio"
	"container/heap"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"

	mapset "github.com/deckarep/golang-set"

	"github.com/mitchellh/hashstructure"
)

type Solution struct {
	Included  []int `hash:"set"`
	SpaceLeft int
	QE        int
	Leftover  []int `hash:"set"`
}

func Exec() {

	file, err := os.Open("input24.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	values := make([]int, 0)

	for {
		line, _, err := reader.ReadLine()

		sline := string(line)

		if err == io.EOF {
			break
		}
		v, _ := strconv.ParseInt(sline, 10, 32)

		values = append(values, int(v))
	}

	//values = []int{1, 2, 3, 4, 5, 7, 8, 9, 10, 11}

	sort.Slice(values, func(i, j int) bool { return values[i] > values[j] })

	var compartmentSize int
	{
		s := 0
		for _, v := range values {
			s += v
		}
		compartmentSize = s / 3
	}

	/*
		// State storage
		states := make(map[uint64]Solution)

		// maps leftover size in comp. 1 to solution set
		compSolutions := make(map[int]mapset.Set)

		put := func(spaceLeft int, s Solution) {
			hash, err := hashstructure.Hash(s, nil)
			if err != nil {
				panic("WTF")
			}
			states[hash] = s
			if _, ok := compSolutions[spaceLeft]; !ok {
				compSolutions[spaceLeft] = mapset.NewSet()
			}
			compSolutions[spaceLeft].Add(hash)
			//fmt.Println("put", spaceLeft, s, hash)
		}

		// Initial state
		initial := Solution{Included: []int{}, QE: 0, Leftover: values}

		put(compartmentSize, initial)

		for spaceLeft := compartmentSize; spaceLeft >= 0; spaceLeft-- {
			if _, ok := compSolutions[spaceLeft]; !ok {
				continue
			}
			fmt.Println("Processing LO", spaceLeft)
			for s := range compSolutions[spaceLeft].Iterator().C {
				//fmt.Println("s", s)
				sh, ok := s.(uint64)
				if !ok {
					panic("WTF")
				}
				solution := states[sh]

				for idx, candidate := range solution.Leftover {
					if spaceLeft-candidate >= 0 {

						head := solution.Leftover[0:idx]
						tail := solution.Leftover[idx+1:]

						newLeftOver := append(append([]int{}, head...), tail...)
						newIncluded := append(append([]int{}, solution.Included...), candidate)

						qe := 1
						for _, s := range newIncluded {
							qe *= s
						}

						newSpaceLeft := spaceLeft - candidate
						put(newSpaceLeft, Solution{Included: newIncluded, QE: qe, Leftover: newLeftOver})
					}
				}
			}
		}
		fmt.Println(compSolutions)

		sortedSolutions := make([]Solution, 0)
	*/

	//currentSolutionLen := len(values)

	QE1 := 0
	var QE1Solution Solution

	for s := range compute(compartmentSize, values) {
		solution := *s
		if testForHalving(compartmentSize, solution.Leftover) {
			QE1 = solution.QE
			QE1Solution = solution
			break
		}
	}

	/*
		for s := range compSolutions[0].Iterator().C {
			sh, ok := s.(uint64)
			if !ok {
				panic("WTF")
			}
			solution := states[sh]

			sortedSolutions = append(sortedSolutions, solution)

			//		fmt.Println(solution)
		}
		sort.Slice(sortedSolutions,
			func(i, j int) bool {
				if len(sortedSolutions[i].Included) < len(sortedSolutions[j].Included) {
					return true
				}
				if len(sortedSolutions[i].Included) > len(sortedSolutions[j].Included) {
					return false
				}
				if sortedSolutions[i].QE < sortedSolutions[j].QE {
					return true
				}
				return false
			},
		)

		QE1 := 0

		for _, v := range sortedSolutions {
			if testForHalving(compartmentSize, v.Leftover) {
				fmt.Println(v)
				QE1 = v.QE
				break
			}
		}

		//fmt.Println(compartmentSize)
	*/
	fmt.Println("Part 1:", QE1, QE1Solution)
	//fmt.Println("Part 2:", calc(1, 0))
}

func testForHalving(compartmentSize int, values []int) bool {
	found := false
	for range compute(compartmentSize, values) {
		found = true
		break
	}
	return found
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Solution

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].SpaceLeft < pq[j].SpaceLeft
}

func (pq *PriorityQueue) Push(x interface{}) {
	item := x.(*Solution)
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

func compute(compartmentSize int, values []int) chan *Solution {

	outputChannel := make(chan *Solution)

	go func(c chan *Solution) {

		pq := make(PriorityQueue, 0)
		heap.Init(&pq)

		// State storage
		states := make(map[uint64]Solution)

		// maps leftover size in a compartment to solution set
		compSolutions := make(map[int]mapset.Set)

		put := func(spaceLeft int, s Solution) bool {
			hash, err := hashstructure.Hash(s, nil)
			if err != nil {
				panic("WTF")
			}
			states[hash] = s
			if _, ok := compSolutions[spaceLeft]; !ok {
				compSolutions[spaceLeft] = mapset.NewSet()
			}
			added := compSolutions[spaceLeft].Add(hash)

			if added && spaceLeft > 0 {
				pq.Push(&s)
			}

			return added
		}

		// Initial state
		initial := Solution{Included: []int{}, SpaceLeft: compartmentSize, QE: 0, Leftover: values}

		put(compartmentSize, initial)

		//for spaceLeft := compartmentSize; spaceLeft > 0; spaceLeft-- {
		for pq.Len() > 0 {

			solution := heap.Pop(&pq).(*Solution)

			for idx, candidate := range solution.Leftover {
				if solution.SpaceLeft-candidate >= 0 {

					head := solution.Leftover[0:idx]
					tail := solution.Leftover[idx+1:]

					newLeftOver := append(append([]int{}, head...), tail...)
					newIncluded := append(append([]int{}, solution.Included...), candidate)

					qe := 1
					for _, s := range newIncluded {
						qe *= s
					}

					newSpaceLeft := solution.SpaceLeft - candidate
					//fmt.Println("newSpaceLeft:", newSpaceLeft)
					newSolution := Solution{Included: newIncluded, SpaceLeft: newSpaceLeft, QE: qe, Leftover: newLeftOver}

					if put(newSpaceLeft, newSolution) && newSpaceLeft == 0 {
						c <- &newSolution
					}
				}
			}
		}
		close(c)
	}(outputChannel)

	return outputChannel
}
