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
	"strconv"
)

var day13 struct {
	// node node cost
	routes map[string]map[string]int
	nodes  []string
}

func Day13() {

	file, err := os.Open("input13.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	day13.nodes = make([]string, 0)
	day13.routes = make(map[string]map[string]int)

	collect := make(map[string]map[string]int)

	for {
		line, _, err := reader.ReadLine()
		sline := string(line)

		r := regexp.MustCompile(`^(?P<src>.+)\swould\s(?P<op>(gain|lose){1})\s(?P<units>[0-9]+)\shappiness.+\sto\s(?P<dst>.+)\.`)

		match := r.FindStringSubmatch(sline)

		paramsMap := make(map[string]string)
		for i, name := range r.SubexpNames() {
			if i > 0 && i <= len(match) {
				paramsMap[name] = match[i]
			}
		}

		if len(paramsMap) == 5 {

			var coef int
			switch paramsMap["op"] {
			case "lose":
				coef = -1
			case "gain":
				coef = 1
			}

			dst := paramsMap["dst"]
			src := paramsMap["src"]
			units, _ := strconv.Atoi(paramsMap["units"])
			cost := units * coef

			if _, ok := collect[dst]; !ok {
				collect[dst] = make(map[string]int)
			}
			if _, ok := collect[src]; !ok {
				collect[src] = make(map[string]int)
			}

			if v, ok := collect[dst][src]; ok {
				collect[dst][src] = cost + v
			} else {
				collect[src][dst] = cost
			}

		}

		if err == io.EOF {
			break
		}
	}

	for k, v := range collect {
		for k1, v1 := range v {
			day13.routes, day13.nodes = common.AddToRoutes(day13.routes, day13.nodes, k, k1, v1)
		}
	}

	p1 := calc13()

	fmt.Println("Part 1:", p1)

	for _, v := range day13.nodes {
		day13.routes, day13.nodes = common.AddToRoutes(day13.routes, day13.nodes, "You", v, 0)
	}

	p2 := calc13()

	fmt.Println("Part 2:", p2)
}

func calc13() int {

	max, err := heldkarp13()

	if err != nil {
		fmt.Println(err)
	}

	return max
}

func heldkarp13() (int, error) {

	nodecount := len(day13.nodes)

	type Choice struct {
		ontheroad []string
		length    int
	}

	// len -> normalizedpath -> struct
	hcandidates := make(map[int]map[string]Choice)

	hcandidates[1] = make(map[string]Choice)

	for _, n := range day13.nodes {
		hcandidates[1][n] = Choice{ontheroad: []string{n}, length: 0}
	}

	for i := 1; i <= nodecount; i++ {
		hcandidates[i+1] = make(map[string]Choice, 0)

		// iterate over current longest paths, generating next longer paths
		for _, this := range hcandidates[i] {

			last := common.Last(this.ontheroad)

			ontheroad := this.ontheroad
			if i == nodecount {
				ontheroad = this.ontheroad[1:]
			}

			// generate all next options
			for nextnode := range common.TSPTakeAll(day13.routes, ontheroad, day13.nodes) {

				nextkey := common.TSPNormalize(this.ontheroad, nextnode)

				// find if this option is minimal S+next
				next, found := hcandidates[i+1][nextkey]

				newlen := this.length + day13.routes[last][nextnode]

				newroad := make([]string, len(ontheroad))
				copy(newroad, ontheroad)
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

	max := math.MinInt32
	for _, v := range hcandidates[nodecount+1] {
		if len(v.ontheroad) == len(day13.nodes) {
			if v.length > max {
				max = v.length
			}
		}
	}

	if max == math.MinInt32 {
		return 0, errors.New("Uups")
	}

	return max, nil
}
