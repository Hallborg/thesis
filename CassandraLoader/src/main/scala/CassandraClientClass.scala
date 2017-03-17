import com.datastax.driver.core.Cluster

/**
  * Created by pps on 2017-02-23.
  */
class CassandraClientClass(var port: Int) {
  private val cluster = Cluster.builder()
    //.addContactPoint("194.47.150.101") //"node 3"
    .addContactPoint("0.0.0.0") //"localhost"
    .withPort(port) // 9042 32776
    .build()

  val session = cluster.connect()

  def execSession(theStr: String) = {
    session.execute(theStr).one()
  }
  def closeCon(): Unit = {
    session.close()
    cluster.close()
  }
  def truncate() : Unit = {
    Seq(
      "TRUNCATE cdr.edr_by_id",
      "TRUNCATE cdr.edr_by_service",
      "TRUNCATE cdr.edr_by_destination",
      "TRUNCATE cdr.edr_by_date"
    ) foreach(session.execute(_))
  }
}
