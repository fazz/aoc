
enum class Dir(val delta: Int) {
    L(-1),
    R(1)
}

fun main() {

    class Step(val write: Int, val dir: Dir, val next: String)

    val rules = hashMapOf(
        "A0" to Step(1, Dir.R, "B"),
        "A1" to Step(0, Dir.L, "C"),

        "B0" to Step(1, Dir.L, "A"),
        "B1" to Step(1, Dir.R, "C"),

        "C0" to Step(1, Dir.R, "A"),
        "C1" to Step(0, Dir.L, "D"),

        "D0" to Step(1, Dir.L, "E"),
        "D1" to Step(1, Dir.L, "C"),

        "E0" to Step(1, Dir.R, "F"),
        "E1" to Step(1, Dir.R, "A"),

        "F0" to Step(1, Dir.R, "A"),
        "F1" to Step(1, Dir.R, "E"),
    )

    val tape = HashMap<Int, Int>()

    val limit = 12261543
    var position = 0
    var step = 0
    var state = "A"


    while(step < limit) {
        val value = tape.getOrDefault(position, 0)

        val key = state + String.format("%d", value)

        val rule = rules.getValue(key)

        tape.put(position, rule.write)

        position += rule.dir.delta
        step++
        state = rule.next
    }

    val part1 = tape
        .filter { e -> e.value == 1 }
        .count()

    System.out.format("Part1: %d\n", part1)

}

