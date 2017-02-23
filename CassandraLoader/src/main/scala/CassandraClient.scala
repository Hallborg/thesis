import com.datastax.driver.core.Cluster

/**
  * Created by pps on 2017-02-09.
  */
object CassandraClient {
  private val cluster = Cluster.builder()
    .addContactPoint("0.0.0.0") //"localhost"
    .withPort(53003) // 9042 32776
    .build()

  val session = cluster.connect()

  def getValueFromCassandraTable() = {
    session.execute("SELECT * FROM myk.users").all()
  }
  def insertValueFromCassandraTable() = {
    session.execute("INSERT into myk.users (id, name, email) VALUES ('1','Jesper','j@gmail.com')")
  }
  def closeCon(): Unit = {
    session.close()
    cluster.close()
  }
}