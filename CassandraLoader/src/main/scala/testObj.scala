
/**
  * Created by pps on 2017-02-09.
  */

object testObj {

  def main(args: Array[String]): Unit = {
    val id_keeper = new IdKeeper
    // Running one thread at the moment. Waiting for three seperate files to load.
    // args(0), 0 is for full load, 1 is for step-wise load
    new Thread(new Loader(args(0).toInt, "../dataModel/mockdata-0.json", 53003, id_keeper)).start
    new Thread(new Loader(args(0).toInt, "../dataModel/mockdata-1.json", 53004, id_keeper)).start
    new Thread(new Loader(args(0).toInt, "../dataModel/mockdata-2.json", 53005, id_keeper)).start

    //Thread.sleep(10000)
    //println(id_keeper.edr_ids.size)
    //id_keeper.edr_ids.foreach(println)
  }
}