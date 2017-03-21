#!/bin/sh

docker run --name $(hostname)-docker -d --net=host -e CASSANDRA_BROADCAST_ADDRESS=192.168.46.13 -e CASSANDRA_SEEDS="192.168.46.11" cassandra:3.9
