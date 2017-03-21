#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR2="$DIR/../cassandra-models"

docker run --name $(hostname)-docker -d --net=host -e CASSANDRA_BROADCAST_ADDRESS=192.168.46.11 -v $DIR2:/cassandra-models cassandra:3.9 #~/thesis/cassandra-models:/cassandra-models
sleep 60
docker exec cont1 cqlsh -e "SOURCE '../cassandra-models/edr.cql'"
#docker run --name cont2 -d -p 53004:9042 -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont1)" cassandra:3
#sleep 60
#docker run --name cont3 -d -p 53005:9042 -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont2)" cassandra:3
#sleep 30
#docker ps
#sleep 30

#sleep 5
#docker exec -i -t cont1 sh -c 'nodetool status' # inspect clusters

#docker run --name cont1 -d -m 1g cassandra

#docker run --name cont2 -d cassandra
#docker run --name cont2 -d -m 1g -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont1)" cassandra
#sleep 30
#docker run --name cont3 -d -m 1g -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont1), $(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont2)" cassandra
#sleep 5
#docker ps
#sleep 30
#docker exec -i -t cont1 sh -c 'nodetool status' # inspect clusters
#sleep 1
#docker exec -i -t cont2 sh -c 'nodetool status'
#sleep 1
#docker exec -i -t cont3 sh -c 'nodetool status'
# docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont1 #find ip


# 55a5678e71b4 55a5678e71b4

#-v private/var/lib/cassandra/c1:/var/lib/cassandra
#docker run -d  -e “CASSANDRA_TOKEN=-9223372036854775808” --name c1 cassandra


#-e “CASSANDRA_TOKEN=-3074457345618258603”

#docker run --name cont1 -d cassandra:3

#docker run --name cont2 -d -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont1)" cassandra:3

#docker run --name cont3 -d -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cont2)" cassandra:3



#docker run -d -v /private/var/lib/cassandra/c1:/private/var/lib/cassandra -e “CASSANDRA_TOKEN=-9223372036854775808” --name c1 cassandra

#docker run --name c2 -v /private/var/lib/cassandra/c2:/private/var/lib/cassandra -d -e “CASSANDRA_TOKEN=-3074457345618258603” -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' c1)" cassandra


#docker run --name c3 -v /private/var/lib/cassandra/c3:/private/var/lib/cassandra -d -e “CASSANDRA_TOKEN=3074457345618258602” -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' c2)" cassandra
