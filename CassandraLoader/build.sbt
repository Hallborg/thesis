name := "CassandraLoader"

version := "1.0"

resolvers += "Typesafe Repo" at "http://repo.typesafe.com/typesafe/releases/"

scalaVersion := "2.11.8"

//libraryDependencies += "com.datastax.cassandra" % "cassandra-driver-core" % "3.1.3"

libraryDependencies ++= Seq("com.typesafe.play" %% "play-json" % "2.3.4",
  "com.datastax.cassandra" % "cassandra-driver-core" % "3.1.3")

enablePlugins(DockerPlugin)

dockerfile in docker := {
  val dockerFiles = {
    val resources = (unmanagedResources in Runtime).value
    val dockerFilesDir = resources.find(_.getPath.endsWith("/docker")).get
    resources.filter(_.getPath.contains("/docker/")).map(r => dockerFilesDir.toURI.relativize(r.toURI).getPath -> r).toMap
  }
  val jarFile: File = sbt.Keys.`package`.in(Compile, packageBin).value
  val classpath = (managedClasspath in Compile).value
  val mainclass = mainClass.in(Compile, packageBin).value.getOrElse(sys.error("Expected exactly one main class"))
  val jarTarget = s"/app/${jarFile.getName}"
  // Make a colon separated classpath with the JAR file
  val classpathString = classpath.files.map("/app/" + _.getName)
    .mkString(":") + ":" + jarTarget
  new Dockerfile {
    // Base image
    from("java")
    // Add all files on the classpath
    add(classpath.files, "/app/")
    add(dockerFiles("data-generator.py"), "~/thesis/dataModel/data-generator.py")
    // Add the JAR file
    add(jarFile, jarTarget)
    // On launch run Java with the classpath and the main class
    entryPoint("java", "-cp", classpathString, mainclass)
  }

}
imageNames in docker := Seq (
  // Sets the latest tag
  ImageName("laban/cassandraloader:latest")
)