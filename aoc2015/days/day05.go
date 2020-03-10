package days

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func Day05() {

	file, err := os.Open("input05.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	count1 := 0
	count2 := 0
	for {
		line, _, err := reader.ReadLine()

		sline := string(line)

		if err == io.EOF {
			break
		}

		// Part 1

		vowels := map[byte]bool{
			'a': true,
			'e': true,
			'i': true,
			'o': true,
			'u': true,
		}

		var pb byte = line[0]

		seq := false

		vc := 0

		double2 := false

		for ix, b := range line {
			if ix <= 13 {
				if line[ix] == line[ix+2] {
					double2 = true
				}
			}

			if _, ok := vowels[b]; ok {
				vc++
			}
			if ix == 0 {
				continue
			}
			if pb == b {
				seq = true
			}
			pb = b
		}

		prohib := strings.Contains(sline, "ab") ||
			strings.Contains(sline, "cd") ||
			strings.Contains(sline, "pq") ||
			strings.Contains(sline, "xy")

		if vc >= 3 && seq && !prohib {
			count1++
		}

		// Part 2

		repeat2 := false
		for ix1, _ := range line[0:13] {
			for ix2, _ := range line[ix1+2 : 15] {
				if (line[ix1] == line[ix2+ix1+2]) && (line[ix1+1] == line[ix2+ix1+3]) {
					repeat2 = true
				}
			}
		}

		if double2 && repeat2 {
			count2++
		}

	}

	fmt.Println("Part 1:", count1)
	fmt.Println("Part 2:", count2)

}
