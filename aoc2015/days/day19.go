package days

import (
	"aoc2015/days/day19"
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strings"
)

func Day19() {

	file, err := os.Open("input19.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	input := ""

	tr := make(map[string][]string)

	takelastline := false
	for {
		line, _, _ := reader.ReadLine()
		sline := string(line)

		if len(sline) == 0 {
			takelastline = true
			continue
		}
		if takelastline {
			input = sline
			break
		}

		r := regexp.MustCompile(`^(?P<src>.+)\s=>\s(?P<dst>.+)`)

		match := r.FindStringSubmatch(sline)

		paramsMap := make(map[string]string)
		for i, name := range r.SubexpNames() {
			if i > 0 && i <= len(match) {
				paramsMap[name] = match[i]
			}
		}

		if len(paramsMap) == 2 {

			src := paramsMap["src"]
			if _, ok := tr[src]; !ok {
				tr[src] = []string{paramsMap["dst"]}
			} else {
				tr[src] = append(tr[src], paramsMap["dst"])
			}
		}
	}

	results := make(map[string]bool)

	for k, v := range tr {
		splits := strings.SplitAfter(input, k)
		for i, s := range splits[:len(splits)-1] {
			for _, dst := range v {
				mod := s[:len(s)-len(k)] + dst
				result := strings.Join(splits[0:i], "") + mod + strings.Join(splits[i+1:], "")
				results[result] = true
			}
		}

	}

	//	fmt.Println("Part 1:", len(results))

	ptoslice := func(i string) []string {

		r := regexp.MustCompile(`([[:upper:]]{1}[[:lower:]]{0,1})`)
		match := r.FindAllString(i, -1)

		return match
	}

	terminals := make(map[string]bool)
	//nonterminals := make(map[string]bool)
	//tokens := make(map[string]bool)

	// Terminals in upper-case
	word := make([]string, 0)
	grammar := make(map[string][][]string)

	for _, w := range ptoslice(input) {
		word = append(word, strings.ToUpper(w))
		terminals[strings.ToUpper(w)] = true
		// Final rule for every terminal
		grammar[strings.ToLower(w)] = [][]string{{strings.ToUpper(w)}}
	}

	for k, v := range tr {
		kl := strings.ToLower(k)
		if _, ok := grammar[kl]; !ok {
			grammar[kl] = make([][]string, 0)
		}

		for _, dst := range v {
			newdst := []string{}
			for _, sym := range ptoslice(dst) {
				newdst = append(newdst, strings.ToLower(sym))
			}
			grammar[kl] = append(grammar[kl], newdst)
		}
	}

	// Synthetic start rule
	grammar["s"] = [][]string{{"e"}}
	parseresult := day19.Parse("s", grammar, word)

	fmt.Println("Part 2:", parseresult.ShortestDerivation-len(word)-1)
	// 605 too high
	// 400 too high

	//
	//
	//

	/*

		for k := range tr {
			nonterminals[k] = true
		}

		for _, t := range ptoslice(input) {
			if _, ok := nonterminals[t]; !ok {
				terminals[t] = true
			}
			tokens[t] = true
		}

		for _, v := range tr {
			for _, dst := range v {
				for _, t := range ptoslice(dst) {
					if _, ok := nonterminals[t]; !ok {
						terminals[t] = true
					}
				}
			}
		}

		fmt.Println("grammar Day19;")
		fmt.Println("// Tokens")

		ccase := func(i string) string {
			if _, ok := tokens[i]; ok {
				return strings.ToUpper(i)
			}
			return strings.ToLower(i)
		}

		tcase := func(i string) string {
			if _, ok := nonterminals[i]; !ok {
				return strings.ToUpper(i)
			}
			return strings.ToLower(i)
		}

		for k := range tokens {
			fmt.Println(strings.ToUpper(k), ": '"+k+"';")
		}

		fmt.Println("// Rules")

		fmt.Println("start : e EOF;")

		for k, v := range tr {

			out := strings.ToLower(k) + " : "

			for i, dst := range v {

				if i > 0 {
					out += " | "
				}

				for i := 0; i <= 1; i++ {

					if i > 0 {
						out += " | "
					}

					for _, d := range ptoslice(dst) {
						if i == 0 {
							out += ccase(d) + " "
						} else {
							out += tcase(d) + " "
						}
					}
					out += "\n"

				}
			}
			//fmt.Println(out + ";")
		}

		//fmt.Println("Part 2:", p2)*/
}
