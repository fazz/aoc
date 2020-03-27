package days

import (
	"aoc2015/common"
	"bufio"
	"errors"
	"fmt"
	"io"
	"math"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var day09 struct {
	// node node cost
	routes map[string]map[string]int
	nodes  []string
}

func add(a, b string, dist int) {
	_, afound := day09.routes[a]
	_, bfound := day09.routes[b]

	if !afound {
		day09.nodes = append(day09.nodes, a)
		day09.routes[a] = make(map[string]int)
	}
	if !bfound {
		day09.nodes = append(day09.nodes, b)
		day09.routes[b] = make(map[string]int)
	}
	day09.routes[a][b] = dist
	day09.routes[b][a] = dist

}

func Day09() {

	file, err := os.Open("input09.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	day09.nodes = make([]string, 0)
	day09.routes = make(map[string]map[string]int)

	for {
		line, _, err := reader.ReadLine()
		sline := string(line)

		r := regexp.MustCompile(`^(?P<src>.+)\sto\s(?P<dst>.+)\s=\s(?P<dist>[0-9]+)`)
		match := r.FindStringSubmatch(sline)

		paramsMap := make(map[string]string)
		for i, name := range r.SubexpNames() {
			if i > 0 && i <= len(match) {
				paramsMap[name] = match[i]
			}
		}

		if len(paramsMap) == 3 {
			dist, _ := strconv.ParseInt(paramsMap["dist"], 10, 32)
			add(paramsMap["dst"], paramsMap["src"], int(dist))
		}

		if err == io.EOF {
			break
		}
	}

	p1, p2 := calc09()

	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}

func calc09() (int, int) {

	min, max, err := heldkarp()

	if err != nil {
		fmt.Println(err)
	}

	return min, max
}

func normalize(path []string, next string) string {
	b := append([]string(nil), path...)
	sort.Strings(b)

	ret := strings.Join(b, "")

	return ret + next
}

func takeall(passed []string, all []string) chan string {
	outputChannel := make(chan string)

	from := common.Last(passed)

	lookup := make(map[string]bool)
	for _, p := range passed {
		lookup[p] = true
	}

	go func() {
		for _, n := range all {
			_, included := lookup[n]
			_, routeexists := day09.routes[from][n]
			if !included && routeexists {
				outputChannel <- n
			}
		}
		close(outputChannel)
	}()
	return outputChannel
}

func heldkarp() (int, int, error) {

	nodecount := len(day09.nodes)

	type Choice struct {
		ontheroad []string
		length    int
	}

	// len -> normalizedpath -> struct
	lcandidates := make(map[int]map[string]Choice)
	hcandidates := make(map[int]map[string]Choice)

	lcandidates[1] = make(map[string]Choice)
	hcandidates[1] = make(map[string]Choice)
	for _, n := range day09.nodes {
		lcandidates[1][n] = Choice{ontheroad: []string{n}, length: 0}
		hcandidates[1][n] = Choice{ontheroad: []string{n}, length: 0}
	}

	for i := 1; i < nodecount; i++ {
		lcandidates[i+1] = make(map[string]Choice, 0)
		hcandidates[i+1] = make(map[string]Choice, 0)

		// iterate over current shortest paths, generating next longer paths
		for _, this := range lcandidates[i] {

			last := common.Last(this.ontheroad)

			// generate all next options
			for nextnode := range takeall(this.ontheroad, day09.nodes) {

				nextkey := normalize(this.ontheroad, nextnode)

				// find if this option is minimal S+next
				next, found := lcandidates[i+1][nextkey]

				newlen := this.length + day09.routes[last][nextnode]
				newroad := make([]string, len(this.ontheroad))
				copy(newroad, this.ontheroad)
				newwinner := Choice{
					ontheroad: append(newroad, nextnode),
					length:    newlen,
				}
				if found {
					if next.length > newlen {
						lcandidates[i+1][nextkey] = newwinner
					}
				} else {
					lcandidates[i+1][nextkey] = newwinner
				}
			}
		}

		// iterate over current longest paths, generating next longer paths
		for _, this := range hcandidates[i] {

			last := common.Last(this.ontheroad)

			// generate all next options
			for nextnode := range takeall(this.ontheroad, day09.nodes) {

				nextkey := normalize(this.ontheroad, nextnode)

				// find if this option is minimal S+next
				next, found := hcandidates[i+1][nextkey]

				newlen := this.length + day09.routes[last][nextnode]
				newroad := make([]string, len(this.ontheroad))
				copy(newroad, this.ontheroad)
				newwinner := Choice{
					ontheroad: append(newroad, nextnode),
					length:    newlen,
				}
				if found {
					if next.length < newlen {
						hcandidates[i+1][nextkey] = newwinner
					}
				} else {
					hcandidates[i+1][nextkey] = newwinner
				}
			}
		}
	}

	min := math.MaxInt32
	for _, v := range lcandidates[nodecount] {
		if len(v.ontheroad) == len(day09.nodes) {
			if v.length < min {
				min = v.length
			}
		}
	}

	max := math.MinInt32
	for _, v := range hcandidates[nodecount] {
		if len(v.ontheroad) == len(day09.nodes) {
			if v.length > max {
				max = v.length
			}
		}
	}

	if min == math.MaxInt32 || max == math.MinInt32 {
		return 0, 0, errors.New("Uups")
	}

	return min, max, nil
}
