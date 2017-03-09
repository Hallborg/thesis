import play.api.libs.json.JsValue

/**
  * Created by Hallborg on 2017-03-09.
  */
object Importer {

  def executeQuery(json: JsValue, con: CassandraClientClass): Unit = {
    val json_part = check_service(json \ ("edr") \ ("service"), json)
    //println(json_part)
    con.execSession(
      "INSERT INTO cdr.edr_by_id JSON '%s!'".format(json_part)
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
