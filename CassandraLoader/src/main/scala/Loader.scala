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

    var text_s = "Strsss test started"
    var text_f = "Stress test stopped"


    val start_date = "date +%s000000000" !!;
    if (setting == 0) {
      json_data.foreach(Importer.executeQuery(_, con))
    }
    else if (setting == 1) {
      text_s = "Step-wise test started"
      text_f = "Step-wise test stopped"
      var start = 0
      var end = 2
      while (end < json_data.size) {
        json_data.slice(start, end) foreach (Importer.executeQuery(_, con))
        start = end
        end = end * 2
        Thread.sleep(500)
      }
      json_data.slice(start, json_data.size) foreach (Importer.executeQuery(_, con))
    }

    val end_date = "date +%s000000"!!;
    val pw = new PrintWriter(new File("../thesis-scripts/" + Thread.currentThread().getName))

    pw.write("alert text='%s' %s".format(text_s, start_date))
    pw.write("alert text='%s' %s".format(text_f, end_date))

    con.closeCon()
    pw.close()


  }
}
