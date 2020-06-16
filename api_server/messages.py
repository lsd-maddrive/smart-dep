import logging
import json
import time
from kombu import Connection, Exchange, Producer


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def init_broker(uri):
    with Connection() as conn:
        channel = conn.channel()
        device_exchange = Exchange('amq.topic', type='topic', durable=True)

        cmd_exchange = Exchange('commands', type='topic', durable=True)
        cmd_exchange.declare(channel=channel)
        device_exchange.bind_to(
            cmd_exchange, routing_key='cmd.*.*', channel=channel)

        cfg_exchange = Exchange('configurations', type='topic', durable=True)
        cfg_exchange.declare(channel=channel)
        device_exchange.bind_to(
            cfg_exchange, routing_key='cfg.*', channel=channel)

        state_exchange = Exchange('states', type='topic', durable=True)
        state_exchange.declare(channel=channel)
        state_exchange.bind_to(
            device_exchange, routing_key='state.*.*', channel=channel)


def ping_device(uri, device_id):
    uri = current_app.config['RABBITMQ_URI']
    logger.debug(f"Connect to RabbitMQ {uri}")
    with Connection(uri) as conn:
        exchange = Exchange('configurations', type='topic', durable=True)
        producer = Producer(exchange=exchange,
                            channel=conn.channel(),
                            routing_key=f'cfg.ping')

        message = json.dumps({
            'device_id': device_id,
            'ts': time.time()
        })
        producer.publish(message)


def reset_device(uri, device_id):
    logger.debug(f"Connect to RabbitMQ {uri}")
    with Connection(uri) as conn:
        exchange = Exchange('configurations', type='topic', durable=True)
        producer = Producer(exchange=exchange,
                            channel=conn.channel(),
                            routing_key=f'cfg.reset')

        message = json.dumps({
            'device_id': device_id,
            'ts': time.time()
        })
        producer.publish(message)


def send_command(uri, device_id, place_id, type_, cmd, source_id):
    logger.debug(f"Connect to RabbitMQ {uri}")

    with Connection(uri) as conn:
        channel = conn.channel()
        exchange = Exchange('commands', type='topic', durable=True)
        producer = Producer(exchange=exchange,
                            channel=channel,
                            routing_key=f'cmd.{place_id}.{type_}')

        message = json.dumps({
            'device_id': device_id,
            'data': cmd,
            'source_id': source_id,
            'ts': time.time()
        })

        producer.publish(message)
    return f'Message sent: {message}'
