package dino

import breeze.linalg._
import akka.actor.{ Actor, ActorLogging, ActorRef, ActorSystem, Props }

object Vertex {
  // def props(dependencies: Array[ActorRef]): Props = Props(new Vertex(dependencies))
  final case class Data(data: DenseMatrix[Double])
}

trait Vertex extends Actor with ActorLogging {
  import Vertex._

  protected var _dependencies: Array[ActorRef]

  def process(matrix: DenseMatrix[Double]): DenseMatrix[Double]

  def send(matrix: DenseMatrix[Double]) = {
    for (dependency <- _dependencies) {
      dependency ! Data(matrix)
    }
  }

  def receive = {
    case Data(matrix) =>
      val result: DenseMatrix[Double] = Utils.time(process(matrix), this.getClass.getName)
      send(result)
  }
}
