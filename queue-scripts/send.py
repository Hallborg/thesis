#!/usr/bin/env python
import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=32769))
channel = connection.channel()

channel.queue_declare(queue='edr')
with open("../dataModel/call_event.json") as source_block:
    call_events = json.load(source_block)

for item in call_events:
    print item["edr"]["id"]
    channel.basic_publish(exchange='',
                         routing_key='edr',
                         body=json.dumps(item))
    print(" [x] Sent one EDR")

connection.close()
