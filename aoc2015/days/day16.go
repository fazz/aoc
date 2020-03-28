package days

import (
	"aoc2015/common"
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func Day16() {

	file, err := os.Open("input16.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	fieldfunc := func(r rune) bool {
		return r == ',' || r == ':'
	}

	choice := "NOTFOUND"

	type Rule struct {
		amount    int64
		predicate func(int64, int64) bool
	}

	rules := make(map[string]Rule)

	for {
		line, _, err := reader.ReadLine()

		sline := string(line)

		if err == io.EOF {
			break
		}

		f := strings.FieldsFunc(sline, fieldfunc)

		aunt := make(map[string]int64)

		aunt[strings.TrimSpace(f[1])], _ = strconv.ParseInt(strings.TrimSpace(f[2]), 10, 16)
		aunt[strings.TrimSpace(f[3])], _ = strconv.ParseInt(strings.TrimSpace(f[4]), 10, 16)
		aunt[strings.TrimSpace(f[5])], _ = strconv.ParseInt(strings.TrimSpace(f[6]), 10, 16)

		rules["children"] = Rule{3, common.Eq}
		rules["cats"] = Rule{7, common.Gt}
		rules["samoyeds"] = Rule{2, common.Eq}
		rules["pomeranians"] = Rule{3, common.Lt}
		rules["akitas"] = Rule{0, common.Eq}
		rules["vizslas"] = Rule{0, common.Eq}
		rules["goldfish"] = Rule{5, common.Lt}
		rules["trees"] = Rule{3, common.Gt}
		rules["cars"] = Rule{2, common.Eq}
		rules["perfumes"] = Rule{1, common.Eq}

		for k, r := range rules {
			if av, ok := aunt[k]; ok {
				if !r.predicate(av, r.amount) {
					goto cont
				}
			}
		}

		choice = f[0]
		break

	cont:
		continue
	}

	fmt.Println("Part 2:", choice)
}
