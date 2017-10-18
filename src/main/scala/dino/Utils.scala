package dino

object Utils {
  val formatter = java.text.NumberFormat.getIntegerInstance
  
  def time[R](block: => R, label: String): R = {
    val t0 = System.nanoTime()
    val result = block
    val t1 = System.nanoTime()
    println(label)
    println("Elapsed time: " + formatter.format(t1 - t0) + "ns\n")
    return result
  }
}
