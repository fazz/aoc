package days

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func Day03() {

	file, err := os.Open("input03.txt")
	if err != nil {
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	buf := make([]byte, 10000)

	readlen, err := reader.Read(buf)

	if err == io.EOF {
		return
	}

	type Vertex struct {
		X int
		Y int
	}

	houses := make(map[Vertex]int)
	houses2 := make(map[Vertex]int)

	v := Vertex{X: 0, Y: 0}

	rs := make(map[int]Vertex)

	rs[0] = v
	rs[1] = v

	houses[v] = 1
	houses2[v] = 1

	for pos := 0; pos < readlen; pos++ {

		char := buf[pos]

		i := pos % 2

		switch char {
		case '^':
			v = Vertex{X: v.X + 0, Y: v.Y - 1}
			rs[i] = Vertex{X: rs[i].X + 0, Y: rs[i].Y - 1}

		case '>':
			v = Vertex{X: v.X + 1, Y: v.Y - 0}
			rs[i] = Vertex{X: rs[i].X + 1, Y: rs[i].Y - 0}

		case '<':
			v = Vertex{X: v.X - 1, Y: v.Y - 0}
			rs[i] = Vertex{X: rs[i].X - 1, Y: rs[i].Y - 0}

		case 'v':
			v = Vertex{X: v.X + 0, Y: v.Y + 1}
			rs[i] = Vertex{X: rs[i].X + 0, Y: rs[i].Y + 1}

		}

		houses[v] = 1
		houses2[rs[i]] = 1
	}

	fmt.Println("Part 1:", len(houses))
	fmt.Println("Part 2:", len(houses2))

}
