
fun main() {

    val state = mutableListOf(14, 0, 15, 12, 11, 11, 3, 5, 1, 6, 8, 4, 9, 1, 8, 4)

    val visited = HashSet<String>()

    val firsts = HashMap<String, Int>()

    var part1 = 0

    var key = state.joinToString("|")

    while (!visited.contains(key)) {
        visited.add(key)
        firsts.put(key, part1)

        var max = 0
        var maxi = 0
        for (i in 0 until state.size) {
            if (state[state.size-i-1] >= max) {
                maxi = state.size-i-1
                max = state[maxi]
            }
        }
        state[maxi] = 0
        var i = (maxi + 1) % state.size
        while (max > 0) {
            state[i]++
            i = (i + 1) % state.size
            max--
        }
        part1++
        key = state.joinToString("|")
    }

    System.out.format("Part1: %d\n", part1)
    System.out.format("Part2: %d\n", part1-firsts.getOrDefault(key, -1))

}
