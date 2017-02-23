/**
  * Created by pps on 2017-02-09.
  */
object testObj {
  def main(args: Array[String]): Unit = {
    println("Hello world")
    CassandraClient.insertValueFromCassandraTable()
    println(CassandraClient.getValueFromCassandraTable())
    CassandraClient.closeCon()
  }
}