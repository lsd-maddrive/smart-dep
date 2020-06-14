import argparse
from datetime import datetime
import json
import logging
import os
import sys

from fluent import handler
import pika
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import threading

from models import Command, Config, State

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

# Setup fluentd connection - simple
custom_format = {
    'host': '%(hostname)s',
    'where': '%(name)s.%(module)s.%(funcName)s',
    'type': '%(levelname)s',
    'stack_trace': '%(exc_text)s'
}

std_h = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d/%H:%M:%S')
std_h.setFormatter(formatter)

fluent_h = handler.FluentHandler('tracker', host='fluentd', port=24224)
formatter = handler.FluentRecordFormatter(custom_format)
fluent_h.setFormatter(formatter)


class Tracker(object):
    def __init__(self, config, exchange_name, binding_key, session):
        self.config = config
        self.session = session
        self.exchange_name = exchange_name

        connection = pika.BlockingConnection(
            pika.URLParameters(self.config["RABBIT_URI"])
        )
        self.channel = connection.channel()

        logger.debug(f"{self.exchange_name} - Connected to rabbit")

        # Declare exchange for logger object
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type='topic',
            durable=True    # Survive a reboot of RabbitMQ
        )

        # Declare exchange to be used by all devices to send messages
        self.channel.exchange_declare(
            exchange="amq.topic",
            exchange_type="topic",
            durable=True    # Survive a reboot of RabbitMQ
        )

        # Declare queue binded to logger exchange
        queue = self.channel.queue_declare(
            queue=f'all_{self.exchange_name}',
            exclusive=False # only allow access by the current connection
        )
        self.queue_name = queue.method.queue

        # Bind queue to amq.topic exchange with correct routing keys
        self.channel.queue_bind(
            queue=f"all_{self.exchange_name}",
            exchange=self.exchange_name,
            routing_key=binding_key
        )

        self.buffer = []
        self.lock = threading.Lock()
        self.timer = None

        self.BUFFER_LIMIT = self.config.get("BUFFER_LIMIT", "1000")
        try:
            self.BUFFER_LIMIT = int(self.BUFFER_LIMIT)
        except Exception as err:
            logger.error(f"Invalid value of BUFFER_LIMIT: {self.BUFFER_LIMIT}")
            raise Exception(f'Configuration of BUFFER_LIMIT contains invalid value: {self.BUFFER_LIMIT}\n{err}')

        self.TIMEOUT_S = self.config.get("TIMEOUT_S", "1.0")
        try:
            self.TIMEOUT_S = float(self.TIMEOUT_S)
        except Exception as err:
            logger.error(f"Invalid value of TIMEOUT: {self.TIMEOUT_S}")
            raise Exception(f'Configuration of TIMEOUT contains invalid value: {self.TIMEOUT_S}\n{err}')

        logger.debug(f"{self.exchange_name} callback is coming to the party\n \
                      Logger Configuration:\n \
                      BUFFER LIMIT: {self.BUFFER_LIMIT}\tTIMEOUT: {self.TIMEOUT_S}")

    def callback(self, ch, method, properties, body):
        in_data = json.loads(body.decode('utf-8'))
        if 'timestamp' not in in_data:
            in_data['timestamp'] = datetime.now()

        new_row = self.get_record(in_data)

        if len(self.buffer) == 0:
            self.start_timer(self.TIMEOUT_S)

        if len(self.buffer) < self.BUFFER_LIMIT:
            self.buffer.append(new_row)

        if len(self.buffer) >= self.BUFFER_LIMIT:
            self.timer.cancel()
            self.send_package_to_db()


    def send_package_to_db(self):
        self.lock.acquire()
        if len(self.buffer) == 0:
            self.lock.release()
            return

        try:
            self.session.bulk_save_objects(
                objects=self.buffer
            )
            self.session.commit()
            logger.debug(f"{self.exchange_name} - Send to DB successfully")
        except Exception as err:
            logger.error(f"{self.exchange_name} - Can not send package to DB\n{err}")
            self.start_timer(self.TIMEOUT_S * 10)
            self.lock.release()
            return

        self.buffer = []
        self.timer.cancel()
        self.lock.release()


    def start_timer(self, period):
        # if timer is dead
        if self.timer is None or not self.timer.is_alive():
            self.timer = threading.Timer(
                interval=period,
                function=self.send_package_to_db
            )
            self.timer.start()

    def consume_event(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True   # automatic acknowledgement mode
        )
        self.channel.start_consuming()

class StateTracker(Tracker):
    def __init__(self, config, session):
        self.binding_key = "state.*.*"
        self.exchange_name = "states"
        super().__init__(
            config, exchange_name=self.exchange_name,
            binding_key=self.binding_key,
            session=session
        )

        # Bind amq.topic exchange -> states exchange
        # self.channel.exchange_bind(
        #     destination=self.exchange_name,
        #     source="amq.topic",
        #     routing_key=self.binding_key
        # )

    def get_record(self, in_data):
        new_state = State(
            timestamp=in_data['timestamp'],
            state=in_data['state'],
            device_id=in_data['device_id'],
        )
        return new_state


class ConfigTracker(Tracker):
    def __init__(self, config, session):
        self.exchange_name = "configurations"
        self.binding_key = "cfg.*"
        super().__init__(
            config, exchange_name=self.exchange_name,
            binding_key=self.binding_key,
            session=session
        )

        # Bind configurations exchange -> amq.topic exchange
        # self.channel.exchange_bind(
        #     destination="amq.topic",
        #     source=self.exchange_name,
        #     routing_key=self.binding_key
        # )

    def get_record(self, in_data):
        new_cgf = Config(
            timestamp=in_data['timestamp'],
            config=in_data.get('data'),
            device_id=in_data['device_id'],
        )
        return new_cgf


class CommandTracker(Tracker):
    def __init__(self, config, session):
        self.exchange_name = "commands"
        self.binding_key = "cmd.*.*"
        super().__init__(
            config, exchange_name=self.exchange_name,
            binding_key=self.binding_key,
            session=session
        )

        # Bind commands exchange -> amq.topic exchange
        # self.channel.exchange_bind(
        #     destination="amq.topic",
        #     source=self.exchange_name,
        #     routing_key=self.binding_key
        # )

    def get_record(self, in_data):
        new_cmd = Command(
            timestamp=in_data['timestamp'],
            command=in_data['data'],
            device_id=in_data['device_id'],
        )
        return new_cmd


def main():
    supported_types = {
        "state": StateTracker,
        "command": CommandTracker,
        "config": ConfigTracker
    }

    type_ = os.getenv('TYPE')
    if type_ not in supported_types:
        logger.critical(f"Logger type has invalid value: {type_}, supported type: {supported_types.keys}")
        return 1

    db_uri = os.getenv('DB_URI')
    if db_uri is None:
        logger.critical("DB URI IS NOT FOUND")
        return 1

    rabbit_uri = os.getenv('RABBITMQ_URI')
    if rabbit_uri is None:
        logger.critical('RABBITMQ URI IS NOT FOUND')
        return 1

    tracker_config = {}
    tracker_config["RABBIT_URI"] = rabbit_uri
    buf_limit = os.getenv("BUFFER_LIMIT")
    if buf_limit is not None:
        tracker_config["BUFFER_LIMIT"] = buf_limit
    timeout = os.getenv("TIMEOUT_S")
    if timeout is not None:
        tracker_config["TIMEOUT_S"] = timeout

    engine = create_engine(db_uri)
    session = Session(engine)

    try:
        tracker_obj = supported_types[type_](tracker_config, session)
        tracker_obj.consume_event()
    except Exception as err:
        logger.error(f"Exception in main loop, reason: {err}")
    finally:
        session.close()
        logger.debug("DB session is CLOSED - successfully!")

    return 0


if __name__ == "__main__":
    sys.exit(main())