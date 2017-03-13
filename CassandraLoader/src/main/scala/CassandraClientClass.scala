import com.datastax.driver.core.Cluster

/**
  * Created by pps on 2017-02-23.
  */
class CassandraClientClass(var port: Int) {
  private val cluster = Cluster.builder()
    .addContactPoint("194.47.150.101") //"localhost"
    .withPort(port) // 9042 32776
    .build()

  val session = cluster.connect()

  def getValueFromCassandraTable() = {
    session.execute("SELECT * FROM myk.users").all()
  }
  def insertValueFromCassandraTable() = {
    session.execute("INSERT into myk.users (id, name, email) VALUES ('1','Jesper','j@gmail.com')")
  }
  def insertValueFromCassandraTable2() = {
    session.execute("INSERT into myk.users (id, name, email) VALUES ('2','Patryk','p@gmail.com')")
  }
  def insertValueFromCassandraTable3() = {
    session.execute("INSERT into myk.users (id, name, email) VALUES ('3','MyNemeIiJeff','jeff@gmail.com')")
  }
  def execSession(theStr: String) = {
    session.execute(theStr).one()
  }
  def closeCon(): Unit = {
    session.close()
    cluster.close()
  }
}
