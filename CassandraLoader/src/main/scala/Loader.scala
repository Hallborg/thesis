import play.api.libs.json.{JsValue, Json}
import sys.process._
import scala.io.Source
import java.io._

/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(setting: Int,thread_name: String, filePath: String, ip: String) {
  val id_keeper = new IdKeeper
  val con = new CassandraClientClass(ip)

  def run_separate(): CassandraClientClass = {

    if (setting == 0) {
      write()
      read()
    }
    else if (setting == 1) {
      step_write(con)
      step_read(con)
    }
    id_keeper.empty()

    con
  }
  def run_mix(): CassandraClientClass = {

    val it = Source.fromFile(filePath).getLines
    if (setting == 0) {
      var i = 0
      for (elem <- it) {
        if(i == 0) Importer.executeWrite(Json.parse(elem), con, id_keeper)
        else if(i % 3 == 0) {
          Importer.executeRead(id_keeper.fetch_random(), con)
        }
        else {
          Importer.executeWrite(Json.parse(elem), con, id_keeper)
        }
        //if (i % 100 == 0) {
          //println(thread_name + " handled mix: " + i)
        //}
        i = i + 1
      }

    }
    else if(setting == 1) step_mix(con)
    con

  }

  def save_time(start_date: String, text_s : String, text_f: String): Unit = {
    val end_date = "date +%s000000000" !!;
    val pw = new FileWriter(new File("../thesis-scripts/" + thread_name), true)

    pw.write("alert text='%s' %s".format(text_s, start_date))
    pw.write("alert text='%s' %s".format(text_f, end_date))
    pw.close()

  }



  def step_write(con: CassandraClientClass): Unit = {
    val it = Source.fromFile(filePath).getLines
    val INC_AMOUNT = 32
    var start = 0
    var end = 31
    var i = 0
    var objects = new scala.collection.mutable.Queue[JsValue]

    for (elem <- it) {
      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (e <- objects) Importer.executeWrite(e, con, id_keeper)

        start = 0
        println(thread_name + " step_wrote: " + (end + 1))
        end = end + INC_AMOUNT

        Thread.sleep(10000 + i * 1000)
	i = i + 1
      }
    }
    println(thread_name + " completed writing, sleeping 20s")
    Thread.sleep(20000)

  }
  def step_read( con: CassandraClientClass): Unit = {
    val it = Source.fromFile(filePath).getLines
    val INC_AMOUNT = 32
    var start = 0
    var end = 31
    var i = 0
    var objects = new scala.collection.mutable.Queue[JsValue]

    for (elem <- it) {
      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (i <- 0 to objects.size) Importer.executeRead(id_keeper.fetch_random(), con)
        start = 0
        println(thread_name + " step_read: " + (end + 1))
        end = end + INC_AMOUNT

        Thread.sleep(10000 + i * 1000)
	i = i + 1
      }

    }

    println(thread_name + " completed reading, sleeping 20s")
    Thread.sleep(20000)
  }

  def step_mix(con: CassandraClientClass): Unit = {
    val it = Source.fromFile(filePath).getLines
    val INC_AMOUNT = 32
    var start = 0
    var end = 31
    var i = 0
    var objects = new scala.collection.mutable.Queue[JsValue]

    for (elem <- it) {
      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (i <- 0 to objects.size) {
          if (i == 0) Importer.executeWrite(objects.dequeue(), con, id_keeper)
          else if(i % 3 == 0) Importer.executeRead(id_keeper.fetch_random(), con)
          else Importer.executeWrite(objects.dequeue(), con, id_keeper)
        }
        start = 0
        println(thread_name + " step_mix: " + (end + 1))
        end = end + INC_AMOUNT

        Thread.sleep(10000 + i * 1000)
	i = i + 1

      }

    }

    println(thread_name + " completed step_reading, sleeping 20s")
    Thread.sleep(20000)
  }

  def write(): Unit = {
    val source = Source.fromFile(filePath).getLines
    var nr_of_runs = 0
    for (elem <- source) {
      Importer.executeWrite(Json.parse(elem), con, id_keeper)
      //if (nr_of_runs % 100 == 0) println(thread_name + " handled write: " + nr_of_runs)
      //nr_of_runs = nr_of_runs + 1
    }
    println(thread_name + "completed writing, sleeping 10s")
    Thread.sleep(10000)

  }

  def read(): Unit = {
    val it_s = Source.fromFile(filePath).getLines.size
    for (i <- 0 to it_s) {
      Importer.executeRead(id_keeper.fetch_random(), con)
      //Importer.executeTestRead(con)
      //if (i % 100 == 0) println(thread_name + " handled read: " + i)
    }
    //save_time(start_date, "Load test -- reading -- started", "Load test -- reading -- ended")
    println(thread_name + "completed reading, sleeping 10s")
    Thread.sleep(10000)
  }

}
