#!/bin/bash

curl -i -XPOST 'http://localhost:8086/write?db=telegraf' --data-binary @$1
