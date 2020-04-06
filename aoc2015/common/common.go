package common

import "sort"

func Lt(x, y int64) bool {
	return x < y
}

func Gt(x, y int64) bool {
	return x > y
}

func Eq(x, y int64) bool {
	return x == y
}

// Max returns the larger of x or y.
func I8Max(x, y int8) int8 {
	if x < y {
		return y
	}
	return x
}

func I64Max(x, y int64) int64 {
	if x < y {
		return y
	}
	return x
}

func IMax(x, y int) int {
	if x < y {
		return y
	}
	return x
}

// Min returns the smaller of x or y.
func I64Min(x, y int64) int64 {
	if x > y {
		return y
	}
	return x
}

func IMin(x, y int) int {
	if x > y {
		return y
	}
	return x
}

func IAbs(x int) int {
	if x < 0 {
		return 0 - x
	}
	return x
}

func Max(x, y int64) int64 {
	if x < y {
		return y
	}
	return x
}

// Min returns the smaller of x or y.
func Min(x, y int64) int64 {
	if x > y {
		return y
	}
	return x
}

func ISwap64(x, y int64) (int64, int64) {
	if x > y {
		t := x
		x = y
		y = t
	}
	return x, y
}

func USwap64(x, y uint64) (uint64, uint64) {
	if x > y {
		t := x
		x = y
		y = t
	}
	return x, y
}

func I8LFold(vs []int8, init int64, f func(int8, int64) int64) int64 {
	r := init
	for _, v := range vs {
		r = f(v, r)
	}
	return r
}

func I8Filter(vs []int8, f func(int8) bool) []int8 {
	vsf := make([]int8, 0)
	for _, v := range vs {
		if f(v) {
			vsf = append(vsf, v)
		}
	}
	return vsf
}

func BFilter(vs []byte, f func(byte) bool) []byte {
	vsf := make([]byte, 0)
	for _, v := range vs {
		if f(v) {
			vsf = append(vsf, v)
		}
	}
	return vsf
}

func Last(i []string) string {
	return i[len(i)-1]
}

func ButLast(i []string) []string {
	return i[:len(i)-1]
}

func IPow(a, b int) int {
	var result int = 1

	for 0 != b {
		if 0 != (b & 1) {
			result *= a

		}
		b >>= 1
		a *= a
	}

	return result
}

// TSP

func AddToRoutes(routes map[string]map[string]int, nodes []string, a, b string, dist int) (map[string]map[string]int, []string) {
	_, afound := routes[a]
	_, bfound := routes[b]

	if !afound {
		nodes = append(nodes, a)
		routes[a] = make(map[string]int)
	}
	if !bfound {
		nodes = append(nodes, b)
		routes[b] = make(map[string]int)
	}
	routes[a][b] = dist
	routes[b][a] = dist

	return routes, nodes
}

func TSPNormalize(path []string, next string) string {
	b := make([]string, len(path))
	copy(b, path)
	sort.Strings(b)

	ret := ""
	for _, s := range b {
		ret += s
	}
	return ret + next
}

func TSPTakeAll(routes map[string]map[string]int, passed []string, all []string) chan string {
	outputChannel := make(chan string)

	from := Last(passed)

	lookup := make(map[string]bool)
	for _, p := range passed {
		lookup[p] = true
	}

	go func() {
		for _, n := range all {
			_, included := lookup[n]
			_, routeexists := routes[from][n]
			if !included && routeexists {
				outputChannel <- n
			}
		}
		close(outputChannel)
	}()
	return outputChannel
}
