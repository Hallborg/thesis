import play.api.libs.json.{JsUndefined, JsValue, Json}

import scala.io.Source
import scala.util.Random
/**
  * Created by Hallborg on 2017-03-14.
  */
class IdKeeper(filePath: String) {
  var temp_json: JsValue = null
  var prev_json: JsValue = null

  val source = Source.fromFile(filePath).getLines

  def populate_ids(json:JsValue): List[String] = {
    temp_json = json
    var dest: JsValue = null
    if ((json \ ("data_event")).isInstanceOf[JsUndefined]) {
      dest = json \ ("call_event") \ ("a_party_location") \ ("destination")
    }
    else {
      dest = json \ ("data_event") \ ("a_party_location") \ ("destination")
    }

    List(
      (json \ "id").toString(),
      (json \ "started_at").toString(),
      dest.toString(),
      (json \ "service").toString(),
      (json \ "created_at").toString()
    )
  }

  def fetch_random(): List[String] = {
    populate_ids(Json.parse(source.next()))
  }

  def fetch_prev(): List[String] = {
    if (prev_json == null) {
      val r = List(
        "\"2015-12-04T18:34:19\"",
        "\"2015-12-04T18:34:19\"",
        "c3467876c7b41efc2dc9b8af0a5d56"
      )
      prev_json = temp_json
      r
    }
    else {
      val r = List(
        (prev_json \ "started_at").toString,
        (prev_json \ "created_at").toString,
        (prev_json \ "id").toString
      )
      prev_json = temp_json
      r
    }
  }
}
