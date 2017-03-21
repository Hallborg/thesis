#!/bin/sh

docker run --name $(hostname)-docker -d --net=host -e CASSANDRA_SEEDS="192.168.46.11" cassandra:3.9
