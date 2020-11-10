package common

fun readFile(fileName: String) =
    object {}.javaClass.getResourceAsStream("/" + fileName).bufferedReader().readLines()
