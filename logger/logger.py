from datetime import datetime  
import json 
import os
import sys 
sys.path.append("..")

from flask_sqlalchemy import SQLAlchemy
import pika 
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import yaml 

from shared.models.table_models import metadata, Commands, Params, States 

with open('config.yml') as cfg:
    total_cfg = yaml.safe_load(cfg)

logger_cfg = total_cfg['logger']
rabbit_cfg = logger_cfg['rabbit']

# TO DO: check 
# FIX for Command and Cfgs (amq.topic -> commands)
# (amq.topic -> configurations)
# self.channel.exchange_bind(
#     destination=topic_name,
#     source="amq.topic"
# )
class Logger(object):
    def __init__(self, config, topic_name, binding_key, session):
        self.config = config 
        self.session = session 
        
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

        # Declare exchange for logger object  
        self.channel.exchange_declare(
            exchange=topic_name,
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
            queue=f'all_{topic_name}', 
            exclusive=False # only allow access by the current connection 
        )
        self.queue_name = queue.method.queue

        # Bind queue to amq.topic exchange with correct routing keys
        self.channel.queue_bind(
            queue=f"all_{topic_name}", 
            exchange=topic_name,
            routing_key=binding_key
        )

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
            config, topic_name=self.exchange_name, 
            binding_key=self.binding_key,
            session=session
        )
        # Bind amq.topic exchange and logger exchange 
        self.channel.exchange_bind(
            destination=self.exchange_name,
            source="amq.topic",
            routing_key=self.binding_key
        )
    
    def callback(self, ch, method, properties, body):
        state_json = json.loads(body.decode('utf-8'))

        if 'timestamp' not in state_json:
            timestamp = datetime.now()
        else:
            timestamp = state_json['timestamp']
        # embedded autoincrement can not track 
        # current changes in DB and use cached values 
        next_id = self.session.query(States).count() + 1
        new_state = States(
            id=next_id,
            timestamp=timestamp,
            state=state_json['state'],
            device_id=state_json['device_id'], 
            place_id=state_json['place_id'],
            type=state_json['type']
        )
        
        self.session.add(new_state)
        self.session.commit()

class ConfigLogger(Logger):
    def __init__(self, config, session):
        self.exchange_name = "configurations"
        self.binding_key = "cfg.*.*"
        super().__init__(
            config, topic_name=self.exchange_name, 
            binding_key=self.binding_key,
            session=session
        )

        # Bind configurations exchange -> amq.topic exchange  
        self.channel.exchange_bind(
            destination="amq.topic",
            source=self.exchange_name,
            routing_key=self.binding_key
        )
    
    def callback(self, ch, method, properties, body):
        cgf_json = json.loads(body.decode('utf-8'))
        if 'timestamp' not in cgf_json:
            timestamp = datetime.now()
        else:
            timestamp = cgf_json['timestamp']
        
        next_id = session.query(Params).count() + 1
        new_cgf = Params(
            id=next_id,
            timestamp=timestamp,
            params=cgf_json['params'],
            device_id=cgf_json['device_id'], 
            place_id=cgf_json['place_id'],
            type=cgf_json['type']
        )
        
        self.session.add(new_cgf)
        self.session.commit()

class CommandLogger(Logger):
    def __init__(self, config, session):
        self.exchange_name = "commands"
        self.binding_key = "cmd.*.*"
        super().__init__(
            config, topic_name=self.exchange_name, 
            binding_key=self.binding_key,
            session=session
        )

        # Bind commands exchange -> amq.topic exchange  
        self.channel.exchange_bind(
            destination="amq.topic",
            source=self.exchange_name,
            routing_key=self.binding_key
        )

    def callback(self, ch, method, properties, body):
        cmd_json = json.loads(body.decode('utf-8'))
        if 'timestamp' not in cmd_json:
            timestamp = datetime.now()
        else:
            timestamp = cmd_json['timestamp']
        
        next_id = session.query(Commands).count() + 1
        new_cmd = Commands(
            id=next_id,
            timestamp=timestamp,
            params=cmd_json['params'],
            device_id=cmd_json['device_id'], 
            place_id=cmd_json['place_id'],
            type=cmd_json['type']
        )
        
        self.session.add(new_cmd)
        self.session.commit()


if __name__ == "__main__":
    # TO DO 
    # FIX config! 
    engine = create_engine('postgresql+psycopg2://admin:admin@tigra:5432/smart_dep')
   
    session = Session(engine)

    session.query(States).delete()
    session.commit()
    # state_logger = StateLogger(rabbit_cfg, session)
    # state_logger.consume_event()
    
    # cfg_logger = ConfigLogger(rabbit_cfg, session)
    # cfg_logger.consume_event()

    # cmd_logger = CommandLogger(rabbit_cfg, session)
    # cmd_logger.consume_event()
    
    # Logger in a waiting loop, this will never be run ??
    session.close()

