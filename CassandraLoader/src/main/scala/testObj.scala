
import scala.io.Source
import java.io.InputStream

//import play.api.libs.iteratee.Execution.Implicits.defaultExecutionContext
///import play.api.libs.json.jackson.JacksonJson
//import org.apache.flink.api.scala._
import play.api.libs.json.Json
import play.api.libs.json._

/**
  * Created by pps on 2017-02-09.
  */
object testObj {
  def main(args: Array[String]): Unit = {
    println("Hello world")
    val con1 = new CassandraClientClass(53003)

    val source: String = Source.fromFile("/Users/pps/Documents/scala/IdeaProjects/thesis/dataModel/call_event.json").getLines.mkString
    val json: JsValue = Json.parse(source)
    val json_str: String = json.toString()
    //println(json_str.charAt(50))
    println(json_str.contains("\"service\":\"1\""))
    //con1.execSession(
    //  "INSERT INTO cdr.edr JSON '%s!' ".format(json)
    //)
    con1.closeCon()
    //con1.execSession(
    //  "TRUNCATE myk.users ;"
    //)
    //con1.insertValueFromCassandraTable()
    //println(con1.getValueFromCassandraTable())

   /* val con2 = new CassandraClientClass(53004)
    con2.insertValueFromCassandraTable2()
    println(con2.getValueFromCassandraTable())

    val con3 = new CassandraClientClass(53005)
    con3.insertValueFromCassandraTable3()
    println(con3.getValueFromCassandraTable())


    println(con1.execSession(
      "SELECT * FROM myk.users WHERE id='2' ; "
    ))
    con1.closeCon()
    println(con2.execSession(
      "SELECT * FROM myk.users WHERE id='3' ; "
    ))
    con2.closeCon()
    println(con3.execSession(
      "SELECT * FROM myk.users WHERE id='1' ;"
    ))
    con3.closeCon()
    //CassandraClient.insertValueFromCassandraTable()
    //println(CassandraClient.getValueFromCassandraTable())
    //CassandraClient.closeCon()*/
  }
}