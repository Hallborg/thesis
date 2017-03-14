import play.api.libs.json.{JsValue, Json}
import sys.process._
import scala.io.Source
import java.io._

/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(setting: Int, filePath: String, port: Int, id_keeper: IdKeeper) extends Runnable {
  def run() = {

    val con = new CassandraClientClass(port)
    val source: String = Source.fromFile(filePath).getLines.mkString
    val json_data: List[JsValue] = Json.parse(source).as[List[JsValue]]


    var start_date = "date +%s000000000" !!;
    if (setting == 0) {
      json_data.foreach(Importer.executeWrite(_, con, id_keeper))
      save_time(start_date, "Load test -- writing -- started", "Load test -- writing -- ended")
      start_date = "date +%s000000000" !!;
      for (i <- 0 to json_data.size) {
        Importer.executeRead(id_keeper.fetch_random(), con)
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

    con.closeCon()
  }

  def save_time(start_date: String, text_s : String, text_f: String): Unit = {
    val end_date = "date +%s000000000" !!;
    val pw = new FileWriter(new File("../thesis-scripts/" + Thread.currentThread().getName), true)

    pw.write("alert text='%s' %s".format(text_s, start_date))
    pw.write("alert text='%s' %s".format(text_f, end_date))
    pw.close()

  }

  def step_write(json_data: List[JsValue], con: CassandraClientClass): Unit = {

    var start = 0
    var end = 2
    while (end < json_data.size) {
      json_data.slice(start, end) foreach (Importer.executeWrite(_, con, id_keeper))
      start = end
      end = end * 2
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
  def step_mix(): Unit = {}
}
