import play.api.libs.json.{JsValue, Json}
import sys.process._
import scala.io.Source
import java.io._

/**
  * Created by Hallborg on 2017-03-09.
  */
class Loader(setting: Int,thread_name: String, filePath: String, ip: String) {
  val INC_AMOUNT = 128
  def run_separate(): Unit = {

    if (setting == 0) {
      write()
      read()
      update()
      delete()
    }
    else if (setting == 1) {
      step_write()
      step_read()
      step_update()
      step_del()
    }
  }
  def run_mix(): Unit = {
    val con = new CassandraClientClass(ip)
    val it = Source.fromFile(filePath).getLines
    if (setting == 0) {
      var i = 0
      for (elem <- it) {
        if(i == 0) Importer.executeWrite(Json.parse(elem), con)
/*        else if(i % 3 == 0) {
          Importer.executeRead(id_keeper.fetch_random(), con)
        }*/
        else {
          Importer.executeWrite(Json.parse(elem), con)
        }
        if (i % 100 == 0) {
          println(thread_name + " handled mix: " + i)
        }
        i = i + 1
      }

    }
    else if(setting == 1) step_mix()

  }



  def step_write(): Unit = {
    val con = new CassandraClientClass(ip)
    val it = Source.fromFile(filePath).getLines
    var start = 0
    var end = 127
    var i = 0
    val objects = new scala.collection.mutable.Queue[JsValue]

    for (elem <- it) {
      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (e <- objects) Importer.executeWrite(e, con)

        start = 0
        println(thread_name + " i:" + i + " step_wrote: " + (end + 1))
        end = end + INC_AMOUNT

        Thread.sleep(6000 + i * 1000)
	      i = i + 1
      }
    }
    println(thread_name + " completed writing, sleeping 20s")
    "shuf %s -o %s".format(filePath, filePath+".read") !!;
    con.closeCon()
    Thread.sleep(20000)

  }
  def step_read(): Unit = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath+".read")
    val it = Source.fromFile(filePath+".read").getLines.size
    var start = 0
    var end = 127
    var i = 0
    var nr_elem = 0

    for (elem <- 0 until it) {
      if ( start <= end) {
        start = start + 1
        nr_elem += 1
      }
      else {
        for (i <- 0 to nr_elem) Importer.executeRead(id_keeper.fetch_random(), con)
        start = 0
        println(thread_name + " step_read: " + (end + 1))
        end = end + INC_AMOUNT
        nr_elem = 0
        Thread.sleep(6000 + i * 1000)
	      i = i + 1
      }

    }

    println(thread_name + " completed reading, sleeping 20s")
    "shuf %s -o %s".format(filePath+".read", filePath+".update") !!;
    con.closeCon()
    Thread.sleep(20000)
  }

  def step_update(): Unit = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath+".update")
    val it = Source.fromFile(filePath+".update").getLines.size
    var start = 0
    var end = 127
    var i = 0
    var nr_elem = 0

    for (elem <- 0 until it) {
      if ( start <= end) {
        start = start + 1
        nr_elem += 1
      }
      else {
        for (i <- 0 to nr_elem) Importer.executeUpdate(id_keeper.fetch_random(),id_keeper.fetch_prev(),con)
        start = 0
        println(thread_name + " step_update: " + (end + 1))
        end = end + INC_AMOUNT
        nr_elem = 0
        Thread.sleep(6000 + i * 1000)
        i = i + 1
      }

    }

    println(thread_name + " completed updating, sleeping 20s")
    "shuf %s -o %s".format(filePath+".update", filePath+".del") !!;
    con.closeCon()
    Thread.sleep(20000)
  }

  def step_del(): Unit = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath+".del")
    val it = Source.fromFile(filePath+".del").getLines.size
    val INC_AMOUNT = 32
    var start = 0
    var end = 127
    var i = 0
    var nr_elem = 0

    for (elem <- 0 until it) {
      if ( start <= end) {
        start = start + 1
        nr_elem += 1
      }
      else {
        for (i <- 0 to nr_elem) Importer.executeDel(id_keeper.fetch_random(),con)
        start = 0
        println(thread_name + " step_del: " + (end + 1))
        end = end + INC_AMOUNT
        nr_elem = 0
        Thread.sleep(6000 + i * 1000)
        i = i + 1
      }

    }

    println(thread_name + " completed deleting, sleeping 20s")
    con.closeCon()
    Thread.sleep(20000)
  }


  def step_mix(): Unit = {
    val con = new CassandraClientClass(ip)
    val it = Source.fromFile(filePath).getLines

    var start = 0
    var end = 127
    var i = 0
    val objects = new scala.collection.mutable.Queue[JsValue]

    for (elem <- it) {
      if ( start <= end) {
        start = start + 1
        objects.enqueue(Json.parse(elem))
      }
      else {
        for (i <- 0 to objects.size) {
          if (i == 0) Importer.executeWrite(objects.dequeue(), con)
          //else if(i % 3 == 0) Importer.executeRead(id_keeper.fetch_random(), con)
          else Importer.executeWrite(objects.dequeue(), con)
        }
        start = 0
        println(thread_name + " step_mix: " + (end + 1))
        end = end + INC_AMOUNT

        Thread.sleep(10000 + i * 1000)
	      i = i + 1

      }

    }

    println(thread_name + " completed step_reading, sleeping 20s")
    con.closeCon()
    Thread.sleep(20000)
  }

  def write(): Unit = {
    val con = new CassandraClientClass(ip)
    val source = Source.fromFile(filePath).getLines

    var nr_of_runs = 0
    for (elem <- source) {
      Importer.executeWrite(Json.parse(elem), con)
      //if (nr_of_runs % 100 == 0) println(thread_name + " handled write: " + nr_of_runs)
      nr_of_runs = nr_of_runs + 1
    }
    println(thread_name + "completed writing, sleeping 10s")
    "shuf %s -o %s".format(filePath, filePath+".read") !!;
    con.closeCon()
    Thread.sleep(10000)

  }

  def read(): Unit = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath+".read")
    val it_s = Source.fromFile(filePath+".read").getLines.size
    for (i <- 0 to it_s -1) {
      Importer.executeRead(id_keeper.fetch_random(), con)
      //if (i % 100 == 0) println(thread_name + " handled read: " + i)
    }

    println(thread_name + "completed reading, sleeping 10s")
    "shuf %s -o %s".format(filePath+".read", filePath+".update") !!;
    con.closeCon()
    Thread.sleep(10000)
  }

  def update() : Unit = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath+".update")
    val it_s = Source.fromFile(filePath+".update").getLines.size
    for(i <- 0 to it_s -1) {
      Importer.executeUpdate(id_keeper.fetch_random(),id_keeper.fetch_prev(),con)
      //if (i % 100 == 0) println(thread_name + "handled update: " + i)
    }
    println(thread_name + "completed updating, sleeping 10s")
    "shuf %s -o %s".format(filePath+".update", filePath+".del") !!;
    con.closeCon()
    Thread.sleep(10000)
  }

  def delete(): Unit = {
    val con = new CassandraClientClass(ip)
    val id_keeper = new IdKeeper(filePath+".del")
    val it_s = Source.fromFile(filePath+".del").getLines.size
    for(i <- 0 to it_s -1) {
      Importer.executeDel(id_keeper.fetch_random(),con)
      //if (i % 100 == 0) println(thread_name + "handled delete: " + i)
    }
    println(thread_name + "completed deleting, sleeping 10s")
    con.closeCon()
    Thread.sleep(10000)
  }

}
