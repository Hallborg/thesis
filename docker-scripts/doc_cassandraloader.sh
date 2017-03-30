#!/bin/sh

# $1 - 0 or 1 to start full load or step-wise
# $2 - cluster contact point (hostname or ip)
# $3 - number of EDRs to create and test with

docker run --rm -it -p 7199:7199 -p 5998:5998 laban/cassandraloader $1 $2 $3