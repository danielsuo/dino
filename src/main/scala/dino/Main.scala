package dino

import breeze.linalg._
import akka.actor.{ Actor, ActorLogging, ActorRef, ActorSystem, Props }
import akka.contrib.pattern.Aggregator
import scala.io.StdIn

object MatrixCreator {
  def props(n: Int, dependencies: Array[ActorRef]): Props = Props(new MatrixCreator(n, dependencies))
}

class MatrixCreator(n: Int, dependencies: Array[ActorRef]) extends Vertex {
  var _dependencies = dependencies

  override def process(matrix: DenseMatrix[Double]): DenseMatrix[Double] = {
    DenseMatrix.rand[Double](n, n)
  }
}

object MatrixTransposer {
  def props(dependencies: Array[ActorRef]): Props = Props(new MatrixTransposer(dependencies))
}

class MatrixTransposer(dependencies: Array[ActorRef]) extends Vertex {
  var _dependencies = dependencies

  override def process(matrix: DenseMatrix[Double]): DenseMatrix[Double] = {
    matrix.t
  }
}

object Main extends App {
  import Vertex._

  val system: ActorSystem = ActorSystem("dino")
  
  val transposer: ActorRef = system.actorOf(MatrixTransposer.props(Array[ActorRef]()), "transpose")
  val creator: ActorRef = system.actorOf(MatrixCreator.props(1000, Array[ActorRef](transposer)), "source")

  var counter = 0
  while (counter < 10) {
    creator ! Data(DenseMatrix.zeros[Double](0, 0))
    counter += 1
  }

  println(">>> Press ENTER to exit <<<")
  StdIn.readLine()

  system.terminate()
}
