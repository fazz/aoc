
package ms07

import common.readFile

fun main() {

    val re = Regex("(\\p{Lower}+) \\((\\p{Digit}+)\\)(?: -> (.+))*$")

    val programs = readFile("input07.txt").map {
        val match = re.find(it)!!.groupValues.toList()

        val name = match[1]
        val weight = match[2]
        val onTop: List<String>
        if (match[3].length > 0) {
            onTop = match[3].split(", ")
        } else {
            onTop = emptyList()
        }

        name to Program(onTop, weight.toInt())
    }.toMap()

    var minInDiffer: Int = 1 shl 30
    var minDifferName = ""
    for (p in programs) {
        p.value.computeTotal(programs)
        if (p.value.difference) {
            if (p.value.totalWeight < minInDiffer) {
                minDifferName = p.key
                minInDiffer = p.value.totalWeight
            }
        }
    }

    val culprit = programs[minDifferName]!!
    val max = culprit.onTop.map {
        programs[it]!!.totalWeight
    }.maxOrNull()!!

    val maxName = culprit.onTop.filter { programs[it]!!.totalWeight == max }.first()

    val min = culprit.onTop.map {
        programs[it]!!.totalWeight
    }.minOrNull()!!

    System.out.format("Part2: %d\n", programs[maxName]!!.weight - (max - min))
}
