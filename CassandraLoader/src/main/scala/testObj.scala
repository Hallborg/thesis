import scala.concurrent
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.{Await, Future}
import sys.process._
import scala.concurrent.duration._
import java.util.Scanner;
/**
  * Created by pps on 2017-02-09.
  */

object testObj {

  def main(args: Array[String]): Unit = {

    // Running one thread at the moment. Waiting for three seperate files to load.
    // args(0), 0 is for full load, 1 is for step-wise load

    val scan = new Scanner(System.in);

	  println("start by typing something")
	  scan.nextLine()

    val loaders = create_loaders(args)


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




    clear_keeper(Await.result(f1, 60 minute), Await.result(f2, 60 minute), Await.result(f3, 60 minute), Await.result(f4, 60 minute))
    println("main thread unblocked")
    val f11 = Future { loaders(0).run_mix() }
    val f12 = Future { loaders(1).run_mix() }
    val f13 = Future { loaders(2).run_mix() }
    val f14 = Future { loaders(3).run_mix() }

    val r1 = Await.result(f11, 60 minute)
    Await.result(f12, 60 minute).closeCon()
    Await.result(f13, 60 minute).closeCon()
    Await.result(f14, 60 minute).closeCon()


    Thread.sleep(5000)
    r1.truncate()
    r1.closeCon()

    println("Test runs completed")


  }
  // need to wait for threads to complete
  def clear_keeper(r1: CassandraClientClass, r2: CassandraClientClass, r3: CassandraClientClass, r4: CassandraClientClass): Unit ={
    println("Truncating database")
    r1.truncate()
    Thread.sleep(5000)
  }

  def create_loaders(args: Array[String]): List[Loader] = {
    if ( args.size == 3 ) {
      println("python ~/thesis/dataModel/data-generator.py %s".format(args(2)) !!)
      List(new Loader(args(0).toInt,"Thread-1", "~/thesis/dataModel/mockdata-0.json", args(1)),
      new Loader(args(0).toInt,"Thread-2", "~/thesis/dataModel/mockdata-1.json", args(1)),
      new Loader(args(0).toInt,"Thread-3", "~/thesis/dataModel/mockdata-2.json", args(1)),
      new Loader(args(0).toInt,"Thread-4", "~/thesis/dataModel/mockdata-3.json", args(1)))
    }
    else {
      List(new Loader(args(0).toInt,"Thread-1", "../dataModel/mockdata-0.json", args(1)),
      new Loader(args(0).toInt,"Thread-2", "../dataModel/mockdata-1.json", args(1)),
      new Loader(args(0).toInt,"Thread-3", "../dataModel/mockdata-2.json", args(1)),
      new Loader(args(0).toInt,"Thread-4", "../dataModel/mockdata-3.json", args(1)))
    }
  }
}
