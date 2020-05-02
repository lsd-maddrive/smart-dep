import argparse 
from datetime import datetime  
import json 
import logging 
import os
import sys 
sys.path.append("..")

from dotenv import load_dotenv
load_dotenv()
import pika 
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import threading
import yaml 

from table_models import metadata, Commands, Configs, States

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

class Logger(object):
    def __init__(self, config, exchange_name, binding_key, session):
        self.config = config 
        self.session = session 
        self.exchange_name = exchange_name
        
        credentials = pika.PlainCredentials(
                username=self.config['username'],
                password=self.config['password']
        )

        params = pika.ConnectionParameters(
                host=self.config['host'],
                port=self.config['port'],
                virtual_host='/',
                credentials=credentials 
        )
        connection = pika.BlockingConnection(params)
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
    
   
    def send_package_to_db(self):
        if len(self.buffer) == 0:
            return 

        self.lock.acquire()

        try:
            self.session.bulk_save_objects(
                objects=self.buffer
            )
            self.session.commit() 
            logger.debug(f"{self.exchange_name} - Send to DB successfully")
        except Exception as err: 
            logger.error(f"{self.exchange_name} - Can not send package to DB\n{err}")
            self.lock.release()
            return 

        self.buffer = []
        self.timer.cancel() 

        self.lock.release()

    def consume_event(self):
        self.channel.basic_consume(
            queue=self.queue_name, 
            on_message_callback=self.callback,
            auto_ack=True   # automatic acknowledgement mode
        )
        self.channel.start_consuming() 

class StateLogger(Logger):
    def __init__(self, config, session):
        self.binding_key = "state.*.*"
        self.exchange_name = "states"
        super().__init__(
            config, exchange_name=self.exchange_name, 
            binding_key=self.binding_key,
            session=session
        )

        # Bind amq.topic exchange -> states exchange 
        self.channel.exchange_bind(
            destination=self.exchange_name,
            source="amq.topic",
            routing_key=self.binding_key
        )

        self.BUFFER_MAX_SIZE = 100 
        self.BUFFER_LIMIT = 10
        self.TIMEOUT_S = 3.0 
    
    def callback(self, ch, method, properties, body):

        logger.debug("StateLogger Callback here")

        state_json = json.loads(body.decode('utf-8'))

        if 'timestamp' not in state_json:
            timestamp = datetime.now()
        else:
            timestamp = state_json['timestamp']
        
        new_state = States(
            timestamp=timestamp,
            state=state_json['state'],
            device_id=state_json['device_id'], 
            place_id=state_json['place_id'],
            type=state_json['type']
        )

        if len(self.buffer) == 0:
            self.timer = threading.Timer(
                interval=self.TIMEOUT_S,
                function=self.send_package_to_db
            )
            self.timer.start() 
        
        self.buffer.append(new_state)

        if len(self.buffer) >= self.BUFFER_LIMIT:
            self.send_package_to_db() 
        
class ConfigLogger(Logger):
    def __init__(self, config, session):
        self.exchange_name = "configurations"
        self.binding_key = "cfg.*.*"
        super().__init__(
            config, exchange_name=self.exchange_name, 
            binding_key=self.binding_key,
            session=session
        )

        # Bind configurations exchange -> amq.topic exchange  
        self.channel.exchange_bind(
            destination="amq.topic",
            source=self.exchange_name,
            routing_key=self.binding_key
        )

        self.BUFFER_MAX_SIZE = 100 
        self.BUFFER_LIMIT = 10
        self.TIMEOUT_S = 3.0 
    
    def callback(self, ch, method, properties, body):

        logger.debug("ConfigLogger Callback here")

        cgf_json = json.loads(body.decode('utf-8'))
        if 'timestamp' not in cgf_json:
            timestamp = datetime.now()
        else:
            timestamp = cgf_json['timestamp']
        
        new_cgf = Configs(
            timestamp=timestamp,
            config=cgf_json['cfg'],
            device_id=cgf_json['device_id'], 
            place_id=cgf_json['place_id'],
            type=cgf_json['type']
        )
        
        if len(self.buffer) == 0:
            self.timer = threading.Timer(
                interval=self.TIMEOUT_S,
                function=self.send_package_to_db
            )
            self.timer.start() 
        
        self.buffer.append(new_cgf)

        if len(self.buffer) >= self.BUFFER_LIMIT:
            self.send_package_to_db() 

class CommandLogger(Logger):
    def __init__(self, config, session):
        self.exchange_name = "commands"
        self.binding_key = "cmd.*.*"
        super().__init__(
            config, exchange_name=self.exchange_name, 
            binding_key=self.binding_key,
            session=session
        )

        # Bind commands exchange -> amq.topic exchange  
        self.channel.exchange_bind(
            destination="amq.topic",
            source=self.exchange_name,
            routing_key=self.binding_key
        )

        self.BUFFER_MAX_SIZE = 100 
        self.BUFFER_LIMIT = 10
        self.TIMEOUT_S = 3.0 

    def callback(self, ch, method, properties, body):

        logger.debug("CommandLogger Callback here")

        cmd_json = json.loads(body.decode('utf-8'))
        if 'timestamp' not in cmd_json:
            timestamp = datetime.now()
        else:
            timestamp = cmd_json['timestamp']
        
        new_cmd = Commands(
            timestamp=timestamp,
            command=cmd_json['cmd'],
            device_id=cmd_json['device_id'], 
            place_id=cmd_json['place_id'],
            type=cmd_json['type']
        )
        
        if len(self.buffer) == 0:
            self.timer = threading.Timer(
                interval=self.TIMEOUT_S,
                function=self.send_package_to_db
            )
            self.timer.start() 

        self.buffer.append(new_cmd)

        if len(self.buffer) >= self.BUFFER_LIMIT:
            self.send_package_to_db() 


if __name__ == "__main__":
    rabbit_cfg = {
        'host': os.getenv('RABBIT_HOST'),
        'port': os.getenv('RABBIT_PORT'),
        'username': os.getenv('RABBIT_USERNAME'),
        'password': os.getenv('RABBIT_PASSWORD')
    }
    
    logger_type = os.getenv('TYPE') 

    logger.debug(f"{logger_type}:\n{rabbit_cfg}\n{os.getenv('DB_URI')}")

    engine = create_engine(os.getenv('DB_URI'))
    session = Session(engine)

    logger.debug(f"Logger session {logger_type} is created successfully!")

    if logger_type == "StateLogger":
        log_Obj = StateLogger(rabbit_cfg, session)
    elif logger_type == "CommandLogger":
        log_Obj = CommandLogger(rabbit_cfg, session)
    elif logger_type == "ConfigLogger":
        log_Obj = ConfigLogger(rabbit_cfg, session)

    log_Obj.consume_event()    

    # session.query(States).delete()
    # session.commit()
    
    session.close()

