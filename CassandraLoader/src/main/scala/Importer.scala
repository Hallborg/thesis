import play.api.libs.json.{JsValue,Json, JsObject}

/**
  * Created by Hallborg on 2017-03-09.
  */
object Importer {


  def executeWrite(json: JsValue, con: CassandraClientClass, id_keeper: IdKeeper): Unit = {
    id_keeper.populate_ids(json)
    val json_part = check_service(json \ ("edr") \ ("service"), json)
    val json_dest_temp = Json.parse(json_part)
    val json_dest: JsObject = json_dest_temp.as[JsObject] +
      ("destination" -> json \ ("edr") \ ("event_details") \ ("a_party_location") \ ("destination"))

    Seq(
      "INSERT INTO cdr.edr_by_id JSON '%s!'".format(json_part),
      "INSERT INTO cdr.edr_by_date JSON '%s!'".format(json_part),
      "INSERT INTO cdr.edr_by_destination JSON '%s!'".format(json_dest),
      "INSERT INTO cdr.edr_by_service JSON '%s!'".format(json_part)
    ) foreach(con.execSession(_))
  }

  def executeRead(keys: List[String], con: CassandraClientClass): Unit = {
    val quries = Seq(
      ("SELECT * FROM cdr.edr_by_id WHERE id = %s".format(keys(0))),
      ("SELECT * FROM cdr.edr_by_destination WHERE destination = %s and id < %s").format(keys(1),keys(0)),
      ("SELECT * FROM cdr.edr_by_service WHERE service = %s and started_at = %s".format(keys(2), keys(3))),
      ("SELECT * FROM cdr.edr_by_date WHERE started_at = %s".format(keys(3)))
    )
    quries map {s => s.replaceAll("\"", "\'")} foreach (con.execSession(_))
  }

  def executeTestRead(con: CassandraClientClass):Unit = {
    println (con.execSession("SELECT * FROM cdr.edr_by_id WHERE id = 'c3467876c7b41efc2dc9b8af0a5d56'"))
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
