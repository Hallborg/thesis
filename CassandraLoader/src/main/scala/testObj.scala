import scala.concurrent
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.{Await, Future}
import sys.process._
import scala.concurrent.duration._
import java.util.Scanner

import scala.io.Source;
/**
  * Created by pps on 2017-02-09.
  */

object testObj {

  def main(args: Array[String]): Unit = {

    // Running one thread at the moment. Waiting for three seperate files to load.
    // args(0), 0 is for full load, 1 is for step-wise load





    val loaders = create_loaders(args)

    if (loaders.size == 1) {
      val f1 = Future {
        loaders(0).run_separate()
      }
      println("main thread blocked")
      Await.result(f1, 60 minute)
    }

    else {
      val f1 = Future {
        loaders(0).run_separate()
      }
      val f2 = Future {
        loaders(1).run_separate()
      }

      val f3 = Future {
        loaders(2).run_separate()
      }

      val f4 = Future {
        loaders(3).run_separate()
      }

      println("main thread blocked")
      calc_sum(args(2), Await.result(f1, 720 minute), Await.result(f2, 720 minute), Await.result(f3, 720 minute), Await.result(f4, 720 minute))
    }

    println("main thread unblocked")
    /*val f11 = Future { loaders(0).run_mix() }
    val f12 = Future { loaders(1).run_mix() }
    val f13 = Future { loaders(2).run_mix() }
    val f14 = Future { loaders(3).run_mix() }

    Await.result(f11, 60 minute)
    Await.result(f12, 60 minute)
    Await.result(f13, 60 minute)
    Await.result(f14, 60 minute)*/


    Thread.sleep(5000)

    println("Test runs completed")


  }
  def calc_sum(ops: String, a: Int, b: Int , c: Int, d: Int) = {
    Seq("bash","-c","echo %s >> %s".format((a+b+c+d),ops))!!
  }

  def create_loaders(args: Array[String]): List[Loader] = {
    val scan = new Scanner(System.in);
    if (args.size == 4) {
      println("start by typing something")
      scan.nextLine()
      if(args(0).toInt == 0) {
        List(new Loader(args(0).toInt,"Thread-1", "/root/thesis/dataModel/mockdata-0", args(1), args(2)),
          new Loader(args(0).toInt,"Thread-2", "/root/thesis/dataModel/mockdata-1", args(1), args(2)),
          new Loader(args(0).toInt,"Thread-3", "/root/thesis/dataModel/mockdata-2", args(1), args(2)),
          new Loader(args(0).toInt,"Thread-4", "/root/thesis/dataModel/mockdata-3", args(1), args(2)))
      }
      else {
        List(new Loader(args(0).toInt,"Thread-1", "~/thesis/dataModel/mockdata-0", args(1), args(2)))
      }

    }
    else {

      println("start by typing something")
      scan.nextLine()
      if(args(0).toInt == 0) {
        List(new Loader(args(0).toInt,"Thread-1", "../dataModel/mockdata-0", args(1), args(2)),
          new Loader(args(0).toInt,"Thread-2", "../dataModel/mockdata-1", args(1), args(2)),
          new Loader(args(0).toInt,"Thread-3", "../dataModel/mockdata-2", args(1), args(2)),
          new Loader(args(0).toInt,"Thread-4", "../dataModel/mockdata-3", args(1), args(2)))
      }
      else {
        List(new Loader(args(0).toInt,"Thread-1", "../dataModel/mockdata-0", args(1), args(2)))
      }

    }
  }
}
