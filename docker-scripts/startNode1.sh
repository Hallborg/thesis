#!/bin/sh
my_ip=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')

volume="-v /root/thesis/doc-cassandra:/var/lib/cassandra"

if [ "$1" = "i" ]; then
    volume=""
fi


docker run --name $(hostname)-docker -d --net=host -p 7000:7000 -p 9042:9042 \
-e CASSANDRA_BROADCAST_ADDRESS=$my_ip -e CASSANDRA_LISTEN_ADDRESS=$my_ip -e \
CASSANDRA_RPC_ADDRESS=$my_ip -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
-e LOCAL_JMX=no -e JVM_OPTS=-Djava.rmi.server.hostname=$my_ip $volume \
laban/cassandra:3.9
sleep 60
cqlsh 192.168.46.11 -e "SOURCE '../cassandra-models/edr.cql'"

#docker run --name $(hostname)-docker -d --net=host -p 7000:7000 -p 9042:9042 -e CASSANDRA_BROADCAST_ADDRESS=192.168.46.11 -v $DIR2:/cassandra-models cassandra:3.9 #~/thesis/cassandra-models:/cassandra-models
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
