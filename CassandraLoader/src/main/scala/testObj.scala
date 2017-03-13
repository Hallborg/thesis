
/**
  * Created by pps on 2017-02-09.
  */

object testObj {
  def main(args: Array[String]): Unit = {

    // Running one thread at the moment. Waiting for three seperate files to load.
    new Thread(new Loader(0, "../dataModel/mockdata-0.json", 53003)).start
    new Thread(new Loader(0, "../dataModel/mockdata-1.json", 53004)).start
    new Thread(new Loader(1, "../dataModel/mockdata-2.json", 53005)).start

  }
}