import play.api.libs.json.{JsValue, Json}

import scala.io.Source

/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(filePath: String, port: Int) extends Runnable {
  def run() = {
    val con = new CassandraClientClass(port)
    val source: String = Source.fromFile(filePath).getLines.mkString
    val json_data: List[JsValue] = Json.parse(source).as[List[JsValue]]

    json_data.foreach(Importer.executeQuery(_, con))
    con.closeCon()
  }
}
