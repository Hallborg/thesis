#!/bin/sh
my_ip=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
first_ip=$(arp -a | head -n 1 | awk '{print $2}' | cut -c 2- | rev | cut -c 2- | rev)

volume="-v /root/thesis/doc-cassandra:/var/lib/cassandra"
if [ "$1" = "i" ]; then
    volume=""
fi

docker run --name $(hostname)-docker -d --net=host -p 7000:7000 -p 9042:9042 \
-e CASSANDRA_BROADCAST_ADDRESS=$my_ip -e CASSANDRA_SEEDS=$first_ip \
-e CASSANDRA_LISTEN_ADDRESS=$my_ip -e CASSANDRA_RPC_ADDRESS=$my_ip \
-e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch\
laban/cassandra:3.9
