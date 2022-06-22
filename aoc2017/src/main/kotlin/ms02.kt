import common.gcd
import common.readFile
import java.lang.Math.*

fun main() {
    val rows = readFile("input02.txt")

    var part1 = 0
    for (r in rows) {
        val elems = r.split(" ", "\t").map{ it.toInt() }
        part1 += abs(elems.maxOf { it } - elems.minOf { it })
    }
    System.out.format("Part1: %d\n", part1)

    var part2 = 0
    for (r in rows) {
        val elems = r.split(" ", "\t").map{ it.toInt() }

        for (i in 0..elems.size-2) {
            for (j in i+1..elems.size-1) {
                val g = gcd(elems[i], elems[j])
                if (g == min(elems[i], elems[j])) {
                    part2 += max(elems[i], elems[j]) / g
                }
            }
        }
    }
    System.out.format("Part2: %d\n", part2)
}
