
/**
  * Created by pps on 2017-02-09.
  */
object testObj {
  def main(args: Array[String]): Unit = {

    // Running one thread at the moment. Waiting for three seperate files to load.
    new Thread(new Loader("../dataModel/mockdata.json", 9042)).start //53003
    // new Thread(new Loader("../dataModel/call_event.json", 53004)).start
    // new Thread(new Loader("../dataModel/call_event.json", 53005)).start
  }
}