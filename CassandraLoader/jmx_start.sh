#!/bin/sh

sbt -Dcom.sun.management.jmxremote \
-Dcom.sun.management.jmxremote.port=7199 \
-Dcom.sun.management.jmxremote.local.only=false \
-Dcom.sun.management.jmxremote.authenticate=false \
-Dcom.sun.management.jmxremote.ssl=false \
-Dcom.sun.management.jmxremote.rmi.port=5998 \
"run $1 192.168.46.11"
