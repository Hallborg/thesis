/**
  * Created by pps on 2017-02-09.
  */
object testObj extends App{
  println("Hello world")
  println(CassandraClient.getValueFromCassandraTable())
  CassandraClient.closeCon()

}