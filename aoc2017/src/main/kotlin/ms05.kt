import common.*

fun main() {

    run {
        val jumps = readFile("input05.txt").map { it.toInt() }.toMutableList()
        var pc = 0
        var part1 = 0

        while (pc >= 0 && pc < jumps.size) {
            part1++
            val j = jumps[pc]
            jumps[pc]++
            pc = pc + j
        }

        System.out.format("Part1: %d\n", part1)
    }

    run {
        val jumps = readFile("input05.txt").map { it.toInt() }.toMutableList()
        var pc = 0

        var part2 = 0

        while (pc >= 0 && pc < jumps.size) {
            part2++
            val j = jumps[pc]
            if (j >= 3) {
                jumps[pc]--
            } else {
                jumps[pc]++
            }
            pc = pc + j
        }

        System.out.format("Part2: %d\n", part2)
    }
}

