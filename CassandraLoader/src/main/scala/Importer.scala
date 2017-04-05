import play.api.libs.json.{JsValue,Json, JsObject}

/**
  * Created by Hallborg on 2017-03-09.
  */
object Importer {


  def executeWrite(json: JsValue, con: CassandraClientClass, id_keeper: IdKeeper): Unit = {
    id_keeper.populate_ids(json)
    val json_dest: JsObject = json.as[JsObject] +
      ("destination" -> json \ ("edr") \ ("event_details") \ ("a_party_location") \ ("destination"))

    Seq(
      "INSERT INTO cdr.edr_by_id JSON '%s!'".format(json),
      "INSERT INTO cdr.edr_by_date JSON '%s!'".format(json),
      "INSERT INTO cdr.edr_by_destination JSON '%s!'".format(json),
      "INSERT INTO cdr.edr_by_service JSON '%s!'".format(json)
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

}
