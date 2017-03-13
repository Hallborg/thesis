import play.api.libs.json.{JsValue, Json}
import sys.process._
import scala.io.Source
import java.io._

/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(setting: Int, filePath: String, port: Int) extends Runnable {
  def run() = {
    val con = new CassandraClientClass(port)
    val source: String = Source.fromFile(filePath).getLines.mkString
    val json_data: List[JsValue] = Json.parse(source).as[List[JsValue]]


    val start_date = "date +%s000000000" !!;
    if (setting == 0) {
      json_data.foreach(Importer.executeWrite(_, con))
      save_time(start_date, "Load test started", "Load test ended")
    }
    else if (setting == 1) {
      val text = step_write(json_data, con)
      save_time(start_date, text(0), text(1))
      step_read(json_data, con)
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
  def step_write(json_data: List[JsValue], con: CassandraClientClass): Seq[String] = {
    val text_s = "Step-wise test started"
    val text_f = "Step-wise test stopped"
    var start = 0
    var end = 2
    while (end < json_data.size) {
      json_data.slice(start, end) foreach (Importer.executeWrite(_, con))
      start = end
      end = end * 2
      Thread.sleep(500)
    }
    json_data.slice(start, json_data.size) foreach (Importer.executeWrite(_, con))

    Seq(text_s, text_f )
  }
  def step_read(json_data: List[JsValue], con: CassandraClientClass): Unit = {}
  def step_mix(): Unit = {}
}
