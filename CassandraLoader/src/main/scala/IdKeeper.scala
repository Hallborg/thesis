import play.api.libs.json.JsValue
import scala.util.Random
/**
  * Created by Hallborg on 2017-03-14.
  */
class IdKeeper {
  val edr_ids = scala.collection.mutable.Set[String]()
  val started_at = scala.collection.mutable.Set[String]()
  val destinations = scala.collection.mutable.Set[String]()
  val services = scala.collection.mutable.Set[String]()


  def populate_ids(json:JsValue): Unit = {
    edr_ids += (json \ ("edr") \ ("id")).toString()
    started_at += (json \ ("edr") \ ("started_at")).toString()
    destinations += (json \ ("edr") \ ("event_details") \ ("a_party_location") \ ("destination")).toString()
    services += (json \("edr") \ ("service")).toString()
  }

  def fetch_random(): List[String] = {
    val rnd = new Random
    List(
      edr_ids.toVector(rnd.nextInt(edr_ids.size)),
      destinations.toVector(rnd.nextInt(destinations.size)),
      services.toVector(rnd.nextInt(services.size)),
      started_at.toVector(rnd.nextInt(started_at.size))
    )
  }

  def empty(): Unit = {
    edr_ids.clear()
    started_at.clear()
    destinations.clear()
    services.clear()

  }
}
