import com.datastax.driver.core.Cluster

/**
  * Created by pps on 2017-02-09.
  */
object CassandraClient {
  private val cluster = Cluster.builder()
    .addContactPoint("localhost")
    .withPort(32776) // 9042
    .build()

  val session = cluster.connect()

  def getValueFromCassandraTable() = {
    session.execute("SELECT * FROM mykeyspace.users").one()
  }
}