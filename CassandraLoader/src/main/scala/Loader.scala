import play.api.libs.json.{JsValue, Json}
import sys.process._
import scala.io.Source
import java.io._
import scala.util.control.Breaks._
import java.util.Calendar
/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(setting: Int,thread_name: String, filePath: String, ip: String, crudOp: String) {
  val INC_AMOUNT = 128
  val EXEC_TIME = 180000
  def run_separate(): Int = {

    if (setting == 0) {
      //"truncate -s 0 %s".format(filePath+".wrote") !!;
      crudOp match {
        case "c" => write()
        case "r" => read()
        case "u" => update()
        case "d" => delete()
      }

    }
    else {
      /*crudOp match {
        case "c" => step_write()
        case "r" => step_read()
        case "u" => step_update()
        case "d" => step_del()
      }*/
      step_mix()
      0
    }
  }
  def run_mix(): Int = {
    val con = new CassandraClientClass(ip)
    val it = Source.fromFile(filePath).getLines
    if (setting == 0) {
      var i = 0
      for (elem <- it) {
        if(i == 0) Importer.executeWrite(Json.parse(elem), con)
/*        else if(i % 3 == 0) {
          Importer.executeRead(id_keeper.fetch_random(), con)
        }*/
        else {
          Importer.executeWrite(Json.parse(elem), con)
        }
        if (i % 100 == 0) {
          println(thread_name + " handled mix: " + i)
        }
        i = i + 1
      }

    }
    else if(setting == 1) step_mix()
    -1
  }



  def step_write(): Int = {
    val con = new CassandraClientClass(ip)
    val it = Source.fromFile(filePath).getLines
    var start = 0
    var end = 127
    var i = 0
    val objects = new scala.collection.mutable.Queue[JsValue]

    for (elem <- it) {
      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (e <- objects) Importer.executeWrite(e, con)

        start = 0
        println(thread_name + " i:" + i + " step_wrote: " + (end + 1))
        end = end + INC_AMOUNT

        Thread.sleep(6000 + i * 1000)
	      i = i + 1
      }
    }
    //println(thread_name + " completed writing, sleeping 20s")
    "shuf %s -o %s".format(filePath, filePath) !!;
    con.closeCon()
    //Thread.sleep(20000)
    -1
  }
  def step_read(): Int = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath)
    val it = Source.fromFile(filePath).getLines.size
    var start = 0
    var end = 127
    var i = 0
    var nr_elem = 0

    for (elem <- 0 until it) {
      if ( start <= end) {
        start = start + 1
        nr_elem += 1
      }
      else {
        for (i <- 0 to nr_elem) Importer.executeRead(id_keeper.fetch_random(), con)
        start = 0
        println(thread_name + " step_read: " + (end + 1))
        end = end + INC_AMOUNT
        nr_elem = 0
        Thread.sleep(6000 + i * 1000)
	      i = i + 1
      }

    }

    //println(thread_name + " completed reading, sleeping 20s")
    "shuf %s -o %s".format(filePath, filePath) !!;
    con.closeCon()
    //Thread.sleep(20000)
    -1
  }

  def step_update(): Int = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath)
    val it = Source.fromFile(filePath).getLines.size
    var start = 0
    var end = 127
    var i = 0
    var nr_elem = 0

    for (elem <- 0 until it) {
      if ( start <= end) {
        start = start + 1
        nr_elem += 1
      }
      else {
        for (i <- 0 to nr_elem) Importer.executeUpdate(id_keeper.fetch_random(),id_keeper.fetch_prev(),con)
        start = 0
        println(thread_name + " step_update: " + (end + 1))
        end = end + INC_AMOUNT
        nr_elem = 0
        Thread.sleep(6000 + i * 1000)
        i = i + 1
      }

    }

    //println(thread_name + " completed updating, sleeping 20s")
    "shuf %s -o %s".format(filePath, filePath) !!;
    con.closeCon()
    //Thread.sleep(20000)
    -1
  }

  def step_del(): Int = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath)
    val it = Source.fromFile(filePath).getLines.size
    var start = 0
    var end = 127
    var i = 0
    var nr_elem = 0

    for (elem <- 0 until it) {
      if ( start <= end) {
        start = start + 1
        nr_elem += 1
      }
      else {
        for (i <- 0 to nr_elem) Importer.executeDel(id_keeper.fetch_random(),con)
        start = 0
        println(thread_name + " step_del: " + (end + 1))
        end = end + INC_AMOUNT
        nr_elem = 0
        Thread.sleep(6000 + i * 1000)
        i = i + 1
      }

    }

    //println(thread_name + " completed deleting, sleeping 20s")
    con.closeCon()
    //Thread.sleep(20000)
    -1
  }


  def step_mix(): Unit = {
    val con = new CassandraClientClass(ip)
    val it = Source.fromFile(filePath).getLines
    val id_keeper = new IdKeeper(filePath)
    var start = 0
    var end = 127
    var i = 0
    val objects = new scala.collection.mutable.Queue[JsValue]

    breakable { for (elem <- it) {

      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (i <- 0 to objects.size) {
          if (i == 0) Importer.executeRead(id_keeper.fetch_random(), con)
          else if(i % 3 == 0) Importer.executeUpdate(id_keeper.fetch_random(),id_keeper.fetch_prev(),con)
          else Importer.executeRead(id_keeper.fetch_random(), con)
        }
        start = 0
        println(thread_name + " step_mix: " + (end + 1))
        end = end + INC_AMOUNT
        if (end == 2687) break
        Thread.sleep(10000 + i * 1000)
	      i = i + 1

      }
      /*val sent = con.session.getCluster.getMetrics.getRequestsTimer.getCount
      val queue = con.session.getCluster.getMetrics.getExecutorQueueDepth.getValue
      println(sent, queue)
      println("nr of responses : " + (queue - sent))*/

    } }
    con.closeCon()
    "shuf %s -o %s".format(filePath, filePath) !!;
    //println(thread_name + " completed step_reading, sleeping 20s")

    //Thread.sleep(20000)
  }

  def write(): Int = {
    val con = new CassandraClientClass(ip)
    val source = Source.fromFile(filePath).getLines
    val date_start = Calendar.getInstance.getTimeInMillis
    var date_stop = Calendar.getInstance.getTimeInMillis
    var nr_of_runs = 0
    var write_rest = false

    breakable {for (elem <- source) {
      if (date_stop >= date_start + EXEC_TIME) break
      Importer.executeWrite(Json.parse(elem), con)
      //if (nr_of_runs % 100 == 0) println(thread_name + " handled write: " + nr_of_runs)
      nr_of_runs = nr_of_runs + 1
      date_stop = Calendar.getInstance.getTimeInMillis
      //if(nr_of_runs % 2 == 0) Thread.sleep(1)
    }}
        //Seq("bash", "-c", "echo '%s' >> %s".format(Json.parse(elem),filePath+".wrote"))!!;



    //println(thread_name + " completed writing rest, sleeping 20s")
    //Seq("bash","-c","echo %s > %s".format(nr_of_runs,thread_name))!!;
    val sent = con.session.getCluster.getMetrics.getRequestsTimer.getCount
    val avg = con.session.getCluster.getMetrics.getRequestsTimer.getOneMinuteRate
    println(sent)
    con.closeCon()
    //Seq("bash","-c","head -n %s %s > %s".format(nr_of_runs,filePath, filePath+".wrote"))!!;
    "shuf %s -o %s".format(filePath, filePath) !!;
    //println(con.nr_of_successful.toDouble / (nr_of_runs*6).toDouble)


    //Thread.sleep(40000)
    0
  }

  def read(): Int = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath)
    val date_start = Calendar.getInstance.getTimeInMillis
    var date_stop = Calendar.getInstance.getTimeInMillis
    var nr_of_runs = 0
    val it_s = Source.fromFile(filePath).getLines.size

    breakable {for (i <- 0 to it_s -1) {
      if (date_stop >= date_start + EXEC_TIME) break
      Importer.executeRead(id_keeper.fetch_random(), con)
      //if (i % 100 == 0) println(thread_name + " handled read: " + i)
      nr_of_runs = nr_of_runs +1
      date_stop = Calendar.getInstance.getTimeInMillis
      //if(nr_of_runs % 2 == 0) Thread.sleep(1)
    }}

    //println(thread_name + " completed reading, sleeping 20s")
    //Seq("bash","-c","echo %s >> %s".format(nr_of_runs,thread_name))!!;

    println(con.session.getCluster.getMetrics.getRequestsTimer.getCount +" "+ nr_of_runs)
    con.closeCon()
    //Thread.sleep(10000)

    "shuf %s -o %s".format(filePath, filePath) !!;
    con.nr_of_successful
  }

  def update() : Int = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath)
    val date_start = Calendar.getInstance.getTimeInMillis
    var date_stop = Calendar.getInstance.getTimeInMillis
    var nr_of_runs = 0
    val it_s = Source.fromFile(filePath).getLines.size

    breakable {for(i <- 0 to it_s -1) {
      if (date_stop >= date_start + EXEC_TIME) break
      Importer.executeUpdate(id_keeper.fetch_random(),id_keeper.fetch_prev(),con)
      //if (i % 100 == 0) println(thread_name + "handled update: " + i)
      nr_of_runs += 1
      date_stop = Calendar.getInstance.getTimeInMillis
      //if(nr_of_runs % 2 == 0) Thread.sleep(1)
    }}
    //println(thread_name + " completed updating, sleeping 20s")
    //Seq("bash","-c","echo %s >> %s".format(nr_of_runs,thread_name))!!;
    println(con.session.getCluster.getMetrics.getRequestsTimer.getCount +" "+ nr_of_runs)
    con.closeCon()
    "shuf %s -o %s".format(filePath, filePath) !!;

    //Thread.sleep(40000)
    con.nr_of_successful
  }

  def delete(): Int = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath)
    val date_start = Calendar.getInstance.getTimeInMillis
    var date_stop = Calendar.getInstance.getTimeInMillis
    var nr_of_runs = 0
    val it_s = Source.fromFile(filePath).getLines.size

    breakable{for(i <- 0 to it_s -1) {
      if (date_stop >= date_start + EXEC_TIME) break
      Importer.executeDel(id_keeper.fetch_random(),con)
      //if (i % 100 == 0) println(thread_name + "handled delete: " + i)
      nr_of_runs += 1
      date_stop = Calendar.getInstance.getTimeInMillis
      //if(nr_of_runs % 2 == 0) Thread.sleep(1)

    }}
    //println(thread_name + " completed deleting, sleeping 10s")
    //Seq("bash","-c","echo %s >> %s".format(nr_of_runs,thread_name))!!;
    //println(thread_name + " completed deleting, sleeping 20s")
    println(con.session.getCluster.getMetrics.getRequestsTimer.getCount +" "+ con.nr_of_successful)
    con.closeCon()
    //Thread.sleep(20000)
    con.nr_of_successful
  }

}
