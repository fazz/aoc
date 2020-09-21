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
	spaceLeft int
	qE        int
	leftOver  []int
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

	sort.Slice(values, func(i, j int) bool { return values[i] > values[j] })

	var compartmentSize1, compartmentSize2 int
	{
		s := 0
		for _, v := range values {
			s += v
		}
		compartmentSize1 = s / 3
		compartmentSize2 = s / 4
	}

	c1 := make(chan int)
	c2 := make(chan int)

	go func(c chan int) {
		var qE int
		for s := range compute(compartmentSize1, values) {
			solution := *s
			qE = solution.qE
			break
		}
		c <- qE
	}(c1)

	go func(c chan int) {
		var qE int
		for s := range compute(compartmentSize2, values) {
			solution := *s
			qE = solution.qE
			break
		}
		c <- qE
	}(c2)

	fmt.Println("Part 1:", <-c1)
	fmt.Println("Part 2:", <-c2)
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Solution

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {

	// First, order by solution len
	if len(pq[i].Included) != len(pq[j].Included) {
		return len(pq[i].Included) < len(pq[j].Included)
	}
	// Then by space left (0 takes precedence)
	if pq[i].spaceLeft != pq[j].spaceLeft {
		return pq[i].spaceLeft < pq[j].spaceLeft
	}

	// When equal (esp. for 0), order by qE
	return pq[i].qE < pq[j].qE
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

	outputChannel := make(chan *Solution, 1)

	go func(c chan *Solution) {

		pq := make(PriorityQueue, 0)
		heap.Init(&pq)

		compSolutions := mapset.NewSet()

		put := func(s Solution) {
			hash, err := hashstructure.Hash(s, nil)
			if err != nil {
				panic("WTF")
			}
			added := compSolutions.Add(hash)

			if added {
				pq.Push(&s)
			}
		}

		// Initial state
		initial := Solution{Included: []int{}, spaceLeft: compartmentSize, qE: 0, leftOver: values}

		put(initial)

		for pq.Len() > 0 {

			solution := heap.Pop(&pq).(*Solution)

			if solution.spaceLeft == 0 {
				c <- solution
			} else {

				for idx, candidate := range solution.leftOver {
					if solution.spaceLeft-candidate >= 0 {

						head := solution.leftOver[0:idx]
						tail := solution.leftOver[idx+1:]

						newLeftOver := append(append([]int{}, head...), tail...)
						newIncluded := append(append([]int{}, solution.Included...), candidate)

						qe := 1
						for _, s := range newIncluded {
							qe *= s
						}

						newSolution := Solution{
							Included:  newIncluded,
							spaceLeft: solution.spaceLeft - candidate,
							qE:        qe,
							leftOver:  newLeftOver,
						}

						put(newSolution)
					}
				}
			}
		}
		close(c)
	}(outputChannel)

	return outputChannel
}
