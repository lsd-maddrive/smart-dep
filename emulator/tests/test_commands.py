from kombu import Connection, Exchange, Producer
import json
import config

conn = Connection(config.RABBITMQ_URI)
channel = conn.channel()
main_exchange = Exchange('commands', type='topic', durable=True)
main_exchange.declare(channel=channel)
device_exchange = Exchange('amq.topic', type='topic', durable=True)
device_exchange.bind_to(main_exchange, routing_key='cmd.*.*', channel=channel)

types = ['light', 'power', 'env']
macs = [
    '01:01:01:01:01:01',
    '11:11:11:11:11:11',
    'F1:F1:F1:F1:F1:F1'
]

for type_ in types:
    for mac in macs:
        data = {
            'type': type_,
            'device_id': mac,
            'place_id': '8201',
            'cmd': {
                'enable': True
            }
        }

        place_id = data['place_id']
        type_ = data['type']
        routing_key = f'cmd.{place_id}.{type_}'
        message = json.dumps(data)

        producer = Producer(exchange=main_exchange,
                            channel=channel, routing_key=routing_key)
        producer.publish(message)
        print(f'Message sent: {message}')
