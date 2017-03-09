#!/usr/bin/env python

import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=32769))
channel = connection.channel()

channel.queue_declare(queue='edr')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    j_bod = json.loads(body)
    print(j_bod["edr"]["id"])

channel.basic_consume(callback,
                      queue='edr',
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
