package common

// Max returns the larger of x or y.
func I8Max(x, y int8) int8 {
	if x < y {
		return y
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
