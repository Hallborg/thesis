name := "CassandraLoader"

version := "1.0"

resolvers += "Typesafe Repo" at "http://repo.typesafe.com/typesafe/releases/"

scalaVersion := "2.10.2"

//libraryDependencies += "com.datastax.cassandra" % "cassandra-driver-core" % "3.1.3"

libraryDependencies ++= Seq("com.typesafe.play" %% "play-json" % "2.3.4",
  "com.datastax.cassandra" % "cassandra-driver-core" % "3.1.3")