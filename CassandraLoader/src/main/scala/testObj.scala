import scala.concurrent
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.{Await, Future}
import scala.util.Success
import scala.concurrent.duration._
/**
  * Created by pps on 2017-02-09.
  */

object testObj {

  def main(args: Array[String]): Unit = {
    val id_keeper = new IdKeeper

    // Running one thread at the moment. Waiting for three seperate files to load.
    // args(0), 0 is for full load, 1 is for step-wise load
    //new Thread(new Loader(args(0).toInt, "../dataModel/mockdata-0.json", 53003, id_keeper)).start()
    //new Thread(new Loader(args(0).toInt, "../dataModel/mockdata-1.json", 53004, id_keeper)).join()
    //new Thread(new Loader(args(0).toInt, "../dataModel/mockdata-2.json", 53005, id_keeper)).join()
    val l1 = new Loader(args(0).toInt,"Thread-1", "../dataModel/mockdata-0.json", "192.168.46.11", id_keeper)
    val l2 = new Loader(args(0).toInt,"Thread-2", "../dataModel/mockdata-1.json", "192.168.46.12", id_keeper)
    val l3 = new Loader(args(0).toInt,"Thread-3", "../dataModel/mockdata-2.json", "192.168.46.13", id_keeper)

    val f1 = Future {
      l1.run_separate()
    }
    val f2 = Future {
      l2.run_separate()
    }

    val f3 = Future {
      l3.run_separate()
    }
    println("main thread blocked")




    clear_keeper(Await.result(f1, 60 second), Await.result(f2, 60 second), Await.result(f3, 60 second), id_keeper)
    println("main thread unblocked")
    val f4 = Future { l1.run_mix() }
    val f5 = Future { l2.run_mix() }
    val f6 = Future { l3.run_mix() }

    val r1 = Await.result(f4, 60 second)
    Await.result(f5, 60 second).closeCon()
    Await.result(f6, 60 second).closeCon()

    Thread.sleep(5000)
    r1.truncate()
    r1.closeCon()

    println("Test runs completed")


  }
  // need to wait for threads to complete
  def clear_keeper(r1: CassandraClientClass, r2: CassandraClientClass, r3: CassandraClientClass, id_keeper: IdKeeper): Unit ={
    id_keeper.empty()
    r1.truncate()
    Thread.sleep(5000)
  }
}