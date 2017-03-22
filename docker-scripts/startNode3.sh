#!/bin/sh

docker run --name $(hostname)-docker -d --net=host -p 7000:7000 -p 9042:9042 -e CASSANDRA_BROADCAST_ADDRESS=192.168.46.13 -e CASSANDRA_SEEDS="192.168.46.11" cassandra:3.9
