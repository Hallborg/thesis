import play.api.libs.json.{JsValue, Json}
import sys.process._
import scala.io.Source
import java.io._

/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(setting: Int,thread_name: String, filePath: String, ip: String, id_keeper: IdKeeper) {
  val con = new CassandraClientClass(ip)
  val source: String = Source.fromFile(filePath).getLines.mkString
  val json_data: List[JsValue] = Json.parse(source).as[List[JsValue]]

  def run_separate(): CassandraClientClass = {
    var nr_of_runs = 0
    var start_date = "date +%s000000000" !!;
    if (setting == 0) {
      for (elem <- json_data) {
        Importer.executeWrite(elem, con, id_keeper)
        if (nr_of_runs % 100 == 0) println(thread_name + " handled write: " + nr_of_runs)
        nr_of_runs = nr_of_runs + 1
      }

      save_time(start_date, "Load test -- writing -- started", "Load test -- writing -- ended")
      start_date = "date +%s000000000" !!;
      for (i <- 0 to json_data.size) {
        Importer.executeRead(id_keeper.fetch_random(), con)
        //Importer.executeTestRead(con)
        if (i % 100 == 0) println(thread_name + " handled read: " + i)
      }
      save_time(start_date, "Load test -- reading -- started", "Load test -- reading -- ended")


    }
    else if (setting == 1) {
      step_write(json_data, con)
      save_time(start_date, "Step-wise test -- writing -- started", "Step-wise test -- writing -- stopped")
      start_date = "date +%s000000000" !!;
      step_read(json_data, con)
      save_time(start_date, "Step-wise test -- reading -- started", "Step-wise test -- reading -- stopped")

    }

    con
  }
  def run_mix(): CassandraClientClass = {

    var start_date = "date +%s000000000" !!;
    if (setting == 0) {
      var i = 0
      for (i <- 0 to json_data.size) {
        if(i == 0) Importer.executeWrite(json_data(0), con, id_keeper)
        else if(i % 3 == 0) {
          Importer.executeRead(id_keeper.fetch_random(), con)
        }
        else {
          Importer.executeWrite(json_data(i), con, id_keeper)
        }
      }
      save_time(start_date, "Load test -- mix -- started", "Load test -- mix -- started")
    }
    else if(setting == 1) {
      step_mix(json_data, con)
      save_time(start_date, "Step-wise test -- mix -- started", "Step-wise test -- mix -- started")

    }
    con

  }

  def save_time(start_date: String, text_s : String, text_f: String): Unit = {
    val end_date = "date +%s000000000" !!;
    val pw = new FileWriter(new File("../thesis-scripts/" + thread_name), true)

    pw.write("alert text='%s' %s".format(text_s, start_date))
    pw.write("alert text='%s' %s".format(text_f, end_date))
    pw.close()

  }

  def step_data_throughput() : Unit = {

  }


  def step_write(json_data: List[JsValue], con: CassandraClientClass): Unit = {

    var start = 0
    var end = 2
    while (end < json_data.size) {
      json_data.slice(start, end) foreach (Importer.executeWrite(_, con, id_keeper))
      start = end
      end = end * 2
      //data_throughput(thread_name, "date +%s000000000" !!)
      Thread.sleep(500)
    }
    json_data.slice(start, json_data.size) foreach (Importer.executeWrite(_, con, id_keeper))

  }
  def step_read(json_data: List[JsValue], con: CassandraClientClass): Unit = {
    var start = 0
    var end = 2
    while (end < json_data.size) {
      Importer.executeRead(id_keeper.fetch_random(), con)
      start = end
      end = end * 2
      Thread.sleep(500)
    }
    for (i <- start to json_data.size) Importer.executeRead(id_keeper.fetch_random(), con)
  }

  def step_mix(json_data: List[JsValue], con: CassandraClientClass): Unit = {
    var start = 0
    var end = 2

    while (end < json_data.size) {
      for (i <- start to end) {
        if (i == 0) Importer.executeWrite(json_data(i), con, id_keeper)
        else if(i % 3 == 0) Importer.executeRead(id_keeper.fetch_random(), con)
        else Importer.executeWrite(json_data(i), con, id_keeper)
      }
      start = end
      end = end * 2
      Thread.sleep(500)

    }
    for (i <- start to json_data.size) {
      if (i == 0) Importer.executeWrite(json_data(i), con, id_keeper)
      else if(i % 3 == 0) Importer.executeRead(id_keeper.fetch_random(), con)
      else Importer.executeWrite(json_data(i), con, id_keeper)
    }
  }
}
