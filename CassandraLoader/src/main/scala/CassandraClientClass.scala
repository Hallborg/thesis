import com.datastax.driver.core.{Cluster, ConsistencyLevel}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.{Await, Future}
import scala.util.{Success, Failure}
import com.datastax.driver.core.QueryOptions
/**
  * Created by pps on 2017-02-23.
  */
class CassandraClientClass(var ip: String) {
  var nr_of_successful = 0
  private val cluster = Cluster.builder()
    //.addContactPoint("194.47.150.101") //"node 3"
    //.withQueryOptions(new QueryOptions().setConsistencyLevel(ConsistencyLevel.TWO))
    .addContactPoint(ip) //"localhost"
    .withPort(9042) // 9042 32776
    .build()

  val session = cluster.connect()

  def execSession(theStr: String) = {

    Future {
      session.executeAsync(theStr).get
    } onComplete {
      case Success(row) => nr_of_successful += 1
      case Failure(t) => 1 + 1
    }
    //Future {
      //session.executeAsync(theStr).get
    //} 
    //session.executeAsync(theStr)
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
