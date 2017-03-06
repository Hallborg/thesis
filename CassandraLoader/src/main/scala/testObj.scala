
import scala.io.Source
import play.api.libs.json.Json
import play.api.libs.json._

/**
  * Created by pps on 2017-02-09.
  */
object testObj {
  def main(args: Array[String]): Unit = {
    println("Hello world")
    val con1 = new CassandraClientClass(53003)

    val source: String = Source.fromFile("../dataModel/call_event.json").getLines.mkString
    val json: List[JsValue] = Json.parse(source).as[List[JsValue]]
    val json_str: String = json.toString()
    /*for (i <- 0 to json.length-1) {
      val value = json.apply(i)
      check_service(value \ ("edr") \ ("service"), json.apply(i))
    }*/
    json.foreach(executeQuery(_, con1))
    // "INSERT INTO cdr.edr JSON '%s!'" ;
    con1.closeCon()

  }

  def executeQuery(json: JsValue, con: CassandraClientClass): Unit = {
    val json_part = check_service(json \ ("edr") \ ("service"), json)
    //println(json_part)
    con.execSession(
      "INSERT INTO cdr.edr JSON '%s!'".format(json_part)
    )
  }

  def check_service(service: JsValue, json: JsValue): String = {
    convert(service) match { //convert(service)
      case 1 => call_event(json)
      case 2 => data_event(json)
    }
  }
  def convert(value: JsValue): Int = {
    value.as[String].toInt
  }
  def call_event(json: JsValue): String = {
    val json_string = (json\("edr")).toString()
    //val temp = json_string.replaceAll("-", "_")
    json_string.replace("\"event_details\"", "\"call_event\"")
  }
  def data_event(json: JsValue): String = {
    val json_string = (json\("edr")).toString()
    //val temp = json_string.replaceAll("-", "_")
    json_string.replace("\"event_details\"", "\"data_event\"")
  }
}