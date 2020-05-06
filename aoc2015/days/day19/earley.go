package day19

import (
	"aoc2015/common"
	"fmt"
	"math"
	"strings"
)

type Data struct {
	Src    string
	Head   []string
	Tail   []string
	Origin int
}

type Complete struct {
	Src        string
	Drv        []string
	Calculated bool
	Cost       int
}

type Source struct {
	Source string
}

type Item struct {
	data    Data
	sources map[string]Source
}

func PrettyPrint(set [][]Item) {

	sp := func(s map[string]Source) string {
		out := ""
		i := 0
		for _, v := range s {
			if i > 0 {
				out += " "
			}
			out += v.Source
			i++
		}
		return out
	}

	fmt.Println()

	for i := 0; i < len(set); i++ {

		fmt.Printf("State: %d\n", i)

		for i, v := range set[i] {
			fmt.Printf("%d\t%01d  %s -> %s * %s\t\tFrom: %s\n", i, v.data.Origin, v.data.Src, v.data.Head, v.data.Tail, sp(v.sources))
		}

	}
	fmt.Println()
}

func normalize(data Data, pos int) string {
	return fmt.Sprintf("%s|%s|%s|%d|%d", data.Src, data.Head, data.Tail, data.Origin, pos)
}

func normalizeC(complete Complete) string {
	return fmt.Sprintf("%s|%s", complete.Src, complete.Drv)
}

func pt(term string) bool {
	return term == strings.ToUpper(term)
}

func minCover(symbols []string, origin, end int, completions map[int]map[int]map[string]*Complete) (int, int) {

	ntstart := 0

	srclen := len(symbols)

	// If terminal, skip
	for ntstart < srclen && pt(symbols[ntstart]) {
		ntstart++
	}

	// All terminals
	if ntstart == srclen {
		return 0, origin + ntstart
	}

	// Find all suitable productions and scan the rest recursively
	symbol := symbols[ntstart]

	mincost := math.MaxInt32
	covered := origin + ntstart

	for prodend := origin + ntstart + 1; prodend <= end; prodend++ {
		if v, ok := completions[origin+ntstart][prodend]; !ok {
			continue
		} else {
			for _, v := range v {
				if v.Src != symbol {
					continue
				}

				if !v.Calculated {
					v.Calculated = true
					c, _ := minCover(v.Drv, origin+ntstart, prodend, completions)
					v.Cost = c + 1
				}
				cost := v.Cost

				if prodend == end {
					mincost = common.IMin(cost, mincost)
					covered = end
				} else if prodend < end {
					c2, e := minCover(symbols[ntstart+1:], prodend, end, completions)
					if e == end {
						mincost = common.IMin(cost+c2, mincost)
						covered = end
					}
				}
			}
		}
	}

	return mincost, covered
}

type ParseResult struct {
	Accepted           bool
	ShortestDerivation int
}

// Parse function implements an Earley parser.
func Parse(start string, grammar map[string][][]string, input []string) ParseResult {

	// end-to-production ,map, items with origin position
	set := make([][]Item, len(input), len(input))
	setidx := make(map[string]int)

	// origin-to-end to production to cost map
	completions := make(map[int]map[int]map[string]*Complete)

	addToSet := func(src string, head, tail []string, origin, pos int, source string) {

		for pos >= len(set) {
			set = append(set, make([]Item, 0, 0))
		}

		data := Data{src, head, tail, origin}

		key := source

		foundidx := 0
		ok := false

		// Rule is already there
		if foundidx, ok = setidx[normalize(data, pos)]; ok {
			set[pos][foundidx].sources[key] = Source{source}
		} else {
			setidx[normalize(data, pos)] = len(set[pos])

			sources := map[string]Source{key: {source}}
			set[pos] = append(set[pos], Item{data: data, sources: sources})
		}

		// Record completions
		if len(data.Tail) == 0 {
			// Init, if needed
			if _, ok = completions[origin]; !ok {
				completions[origin] = make(map[int]map[string]*Complete)
			}
			if _, ok = completions[origin][pos]; !ok {
				completions[origin][pos] = make(map[string]*Complete)
			}

			complete := Complete{src, head, false, math.MaxInt32}
			key := normalizeC(complete)
			if _, ok := completions[origin][pos][key]; !ok {
				completions[origin][pos][key] = &complete
			}
		}
	}

	// artificial first rule
	addToSet(start, []string{}, grammar[start][0], 0, 0, "Start")

	predictor := func(state Item, pos, idx int, sources map[string]Source) {
		rules := grammar[state.data.Tail[0]]
		for _, r := range rules {
			addToSet(state.data.Tail[0], []string{}, r, pos, pos, fmt.Sprintf("Predict %d/%d", pos, idx))
		}
	}

	scanner := func(state Item, pos, idx int, sources map[string]Source) {
		word := state.data.Tail[0]
		if pos < len(input) && word == input[pos] {

			head := append([]string(nil), state.data.Head...)
			tail := append([]string(nil), state.data.Tail...)
			head = append(head, tail[0])
			tail = tail[1:]

			addToSet(state.data.Src, head, tail, state.data.Origin, pos+1, fmt.Sprintf("Scan %d/%d", pos, idx))
		}
	}

	completer := func(state Item, pos, idx int, sources map[string]Source) {
		for _, v := range set[state.data.Origin] {
			if len(v.data.Tail) > 0 && v.data.Tail[0] == state.data.Src {

				head := append([]string(nil), v.data.Head...)
				tail := append([]string(nil), v.data.Tail...)
				head = append(head, tail[0])
				tail = tail[1:]

				addToSet(v.data.Src, head, tail, v.data.Origin, pos, fmt.Sprintf("Compl %d/%d", pos, idx))
			}
		}
	}

	// iterate over gaps in input
	for pos := 0; pos <= len(input); pos++ {

		i := 0

		for pos < len(set) && i < len(set[pos]) {
			// Finished
			if len(set[pos][i].data.Tail) == 0 {
				// Completer
				completer(set[pos][i], pos, i, set[pos][i].sources)
			} else {
				if pt(set[pos][i].data.Tail[0]) {
					// Scanner
					scanner(set[pos][i], pos, i, set[pos][i].sources)
				} else {
					// Predictor
					predictor(set[pos][i], pos, i, set[pos][i].sources)
				}
			}
			i++
		}
	}

	//PrettyPrint(set)

	result := ParseResult{ShortestDerivation: math.MaxInt32}

	complete := Complete{start, []string{grammar[start][0][0]}, false, 0}

	// Accepted
	if c, ok := completions[0][len(input)][normalizeC(complete)]; ok {
		result.Accepted = true

		// Calculation
		count, _ := minCover(c.Drv, 0, len(input), completions)
		result.ShortestDerivation = count + 1
	}

	return result
}
