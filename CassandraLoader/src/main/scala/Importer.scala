import play.api.libs.json.{JsObject, JsUndefined, JsValue, Json}

/**
  * Created by Hallborg on 2017-03-09.
  */
object Importer {

//behövs formateringen?
  def executeWrite(json: JsValue, con: CassandraClientClass): Unit = {
    var dest: JsValue = null
    if ((json \ "data_event").isInstanceOf[JsUndefined]) {
      dest = json \ "call_event" \ "a_party_location" \ "destination"
    }
    else {
      dest = json \ "data_event" \ "a_party_location" \ "destination"
    }
    val json_dest: JsObject = json.as[JsObject] +
      ("destination" -> dest)

    Seq(
      "INSERT INTO cdr.edr_by_id JSON '%s!'".format(json),
      "INSERT INTO cdr.edr_by_date JSON '%s!'".format(json),
      "INSERT INTO cdr.edr_by_destination JSON '%s!'".format(json_dest),
      "INSERT INTO cdr.edr_by_service JSON '%s!'".format(json)
    ) foreach(con.execSession(_))
  }

  def executeRead(keys: List[String], con: CassandraClientClass): Unit = {
    Seq(
      "SELECT * FROM cdr.edr_by_id WHERE id = %s".format(keys.head),
      "SELECT * FROM cdr.edr_by_destination WHERE destination = %s and id < %s".format(keys(2),keys.head),
      "SELECT * FROM cdr.edr_by_service WHERE service = %s and started_at = %s".format(keys(3), keys(1)),
      "SELECT * FROM cdr.edr_by_date WHERE started_at = %s".format(keys(1))
    ) map {s => s.replaceAll("\"", "\'")} foreach (con.execSession(_))
  }
  def executeUpdate(keys: List[String], new_vals: List[String], con:CassandraClientClass):Unit = {
    Seq(
      "UPDATE cdr.edr_by_id SET started_at = %s WHERE id = %s".format(new_vals.head, keys.head),
      "UPDATE cdr.edr_by_destination SET started_at = %s WHERE destination = %s and id = %s".format(new_vals.head, keys(2), keys.head),
      "UPDATE cdr.edr_by_service SET created_at = %s WHERE service = %s and started_at = %s".format(new_vals(1), keys(3), keys(1)),
      "UPDATE cdr.edr_by_date SET created_at = %s WHERE started_at = %s and id = %s".format(new_vals(1), keys(3), keys.head)


    ) map {s => s.replaceAll("\"", "\'")} foreach (con.execSession(_))
  }
  def executeDel(keys: List[String], con: CassandraClientClass): Unit = {
    Seq(
      "DELETE FROM cdr.edr_by_id WHERE id = %s".format(keys.head),
      "DELETE FROM cdr.edr_by_destination where destination = %s AND id = %s".format(keys(2),keys.head),
      "DELETE FROM cdr.edr_by_service WHERE service = %s AND started_at = %s".format(keys(3), keys(1)),
      "DELETE FROM cdr.edr_by_date WHERE started_at = %s AND id = %s".format(keys(1), keys.head)
    ) map {s => s.replaceAll("\"", "\'")} foreach (con.execSession(_))
  }

  def executeTestRead(con: CassandraClientClass): Unit = {
    println (con.execSession("SELECT * FROM cdr.edr_by_id WHERE id = 'c3467876c7b41efc2dc9b8af0a5d56'"))
  }

  /*def check_service(service: JsValue, json: JsValue): String = {
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
  }*/

}
