#!/bin/sh

docker ps
docker exec -i -t $(hostname)-docker sh -c 'nodetool status' # inspect clusters