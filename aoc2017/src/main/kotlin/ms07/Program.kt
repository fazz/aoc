package ms07

import kotlin.math.absoluteValue

class Program(val onTop: List<String>, val weight: Int) {

    fun computeTotal(programs: Map<String, Program>): Int {
        var singleWeight: Int? = null

        if (totalWeight == -1) {
            totalWeight = weight
            for (t in onTop) {
                val v = programs[t]!!.computeTotal(programs)

                if (singleWeight != null) {
                    if (v != singleWeight) {
                        this.difference = true
                    }
                } else {
                    singleWeight = v
                }
                totalWeight += v
            }
        }
        return totalWeight
    }

    var totalWeight: Int = -1
    var difference = false
}
