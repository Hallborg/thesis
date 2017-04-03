import play.api.libs.json.JsValue
import scala.util.Random
/**
  * Created by Hallborg on 2017-03-14.
  */
class IdKeeper {
  val edr_ids = scala.collection.mutable.ArrayBuffer[String]()
  val started_at = scala.collection.mutable.ArrayBuffer[String]()
  val destinations = scala.collection.mutable.ArrayBuffer[String]()
  val services = scala.collection.mutable.ArrayBuffer[String]()
  val rnd = new Random

  def populate_ids(json:JsValue): Unit = {
    edr_ids += (json \ ("edr") \ ("id")).toString()
    started_at += (json \ ("edr") \ ("started_at")).toString()
    destinations += (json \ ("edr") \ ("event_details") \ ("a_party_location") \ ("destination")).toString()
    services += (json \("edr") \ ("service")).toString()
  }

  def fetch_random(): List[String] = {
    List(
      edr_ids(rnd.nextInt(edr_ids.size)),
      destinations(rnd.nextInt(destinations.size)),
      services(rnd.nextInt(services.size)),
      started_at(rnd.nextInt(started_at.size))
    )
  }

  def empty(): Unit = {
    edr_ids.clear()
    started_at.clear()
    destinations.clear()
    services.clear()

  }
}
