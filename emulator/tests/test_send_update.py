from kombu import Connection, Exchange, Producer
import json
import config

with Connection(config.RABBITMQ_URI) as connection:
    channel = connection.channel()

    main_exchange = Exchange('configurations', type='topic', durable=True)
    main_exchange.declare(channel=channel)
    device_exchange = Exchange('amq.topic', type='topic', durable=True)
    device_exchange.bind_to(main_exchange, routing_key='cfg.*', channel=channel)

    with open('code.py') as f:
        module_str = f.read()

    message = json.dumps({
        'code': module_str,
        'device_id': '1234567890qwerty'
    })

    producer = Producer(exchange=main_exchange,
                        channel=channel,
                        routing_key=f'cfg.updates')
    producer.publish(message)
    print(f'Message sent: {message}')
