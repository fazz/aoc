package common

fun readFile(fileName: String) =
    object {}.javaClass.getResourceAsStream("/" + fileName).bufferedReader().readLines()

fun gcd(x: Int, y: Int): Int {
    var a = x
    var b = y
    while (b != 0) {
        val t = b
        b = a % b
        a = t
    }
    return a
}