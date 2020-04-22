import pika 
from pprint import pprint
import yaml 

with open('config.yml') as cfg:
    total_cfg = yaml.safe_load(cfg)

logger_cfg = total_cfg['logger']
rabbit_cfg = logger_cfg['rabbit']

credentials = pika.PlainCredentials(
    username=rabbit_cfg['username'],
    password=rabbit_cfg['password']
)

params = pika.ConnectionParameters(
    host=rabbit_cfg['host'],
    port=rabbit_cfg['port'],
    virtual_host='/',
    credentials=credentials 
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

class Logger(object):
    def __init__(self, config, topic_name):
        self.config = config 
        
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
        channel = connection.channel()

        channel.exchange_declare(
            exchange=topic_name,
            exchange_type='topic'
        )

        queue = channel.queue_declare(
            queue='', # random name for queue
            exclusive=True # only allow access by the current connection 
        )

        binding_keys = []