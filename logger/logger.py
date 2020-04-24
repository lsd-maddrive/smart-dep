import pika 
from pprint import pprint
import yaml 

# with open('config.yml') as cfg:
#     total_cfg = yaml.safe_load(cfg)

# logger_cfg = total_cfg['logger']
# rabbit_cfg = logger_cfg['rabbit']

# credentials = pika.PlainCredentials(
#     username=rabbit_cfg['username'],
#     password=rabbit_cfg['password']
# )

# params = pika.ConnectionParameters(
#     host=rabbit_cfg['host'],
#     port=rabbit_cfg['port'],
#     virtual_host='/',
#     credentials=credentials 
# )


class Logger(object):
    def __init__(self, config, topic_name, binding_keys):
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
        self.channel = connection.channel()

        self.channel.exchange_declare(
            exchange=topic_name,
            exchange_type='topic'
        )

        queue = self.channel.queue_declare(
            queue=f'all_{topic_name}', 
            exclusive=True # only allow access by the current connection 
        )

        self.queue_name = queue.method.queue

        self.channel.queue_bind(
            exchange=topic_name, 
            queue=queue_name,
            routing_key=binding_keys
        )

    def callback():
        pass 

    def consume_event():
        self.channel.basic_consume(
            queue=self.queue_name, 
            on_message_callback=self.callback,
            auto_ack=True
        )

        self.channel.start_consuming() 

class StateLogger(Logger):
    def __init__(self, config):
        super().__init__(
            config, topic_name="states", 
            binding_keys=[
                "state.*.light",
                "state.*.power",
                "state.*.env"
            ]
        )
    
    def callback():
        pass 

class ConfigLogger(Logger):
    def __init__(self, config):
        super().__init__(
            config, topic_name="configurations", 
            binding_keys=[
                "cfg.*.light",
                "cfg.*.power",
                "cfg.*.env"
            ]
        )
    
    def callback():
        pass 

class CommandLogger(Logger):
    def __init__(self, config):
        super().__init__(
            config, topic_name="commands", 
            binding_keys=[
                "cmd.*.light",
                "cmd.*.power",
                "cmd.*.env"
            ]
        )

    def callback():
        pass 
