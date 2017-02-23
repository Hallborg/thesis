/**
  * Created by pps on 2017-02-09.
  */
object testObj {
  def main(args: Array[String]): Unit = {
    println("Hello world")
    val con1 = new CassandraClientClass(53003)
    con1.execSession(
      "TRUNCATE myk.users ;"
    )
    con1.insertValueFromCassandraTable()
    println(con1.getValueFromCassandraTable())


    val con2 = new CassandraClientClass(53004)
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
    //CassandraClient.closeCon()
  }
}