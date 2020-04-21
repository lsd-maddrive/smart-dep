from kombu import Connection, Exchange, Queue, Consumer, eventloop
import json
from pprint import pformat
import config

conn = Connection(config.RABBITMQ_URI)
channel = conn.channel()
main_exchange = Exchange('states', type='topic', durable=True)
main_exchange.declare(channel=channel)
device_exchange = Exchange('amq.topic', type='topic', durable=True)
main_exchange.bind_to(device_exchange, routing_key='state.*.*', channel=channel)

queue = Queue('all_states', main_exchange, routing_key='#', durable=False)


def pretty(obj):
    return pformat(obj, indent=4)


def handle_message(body, message):
    print('Received message: {0!r}'.format(body))
    print('  properties:\n{0}'.format(pretty(message.properties)))
    print('  delivery_info:\n{0}'.format(pretty(message.delivery_info)))
    message.ack()


with Connection(config.RABBITMQ_URI) as connection:

    #: Create consumer using our callback and queue.
    #: Second argument can also be a list to consume from
    #: any number of queues.
    with Consumer(connection, queue, callbacks=[handle_message]):

        #: Each iteration waits for a single event.  Note that this
        #: event may not be a message, or a message that is to be
        #: delivered to the consumers channel, but any event received
        #: on the connection.
        for _ in eventloop(connection):
            pass


