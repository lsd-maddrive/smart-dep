import time
import math as m


class Code():
    def __init__(self, config):
        self.config = config
        self.device_id = config['device_id']
        self.place_id = config['place_id']
        self.type = config['type']
        self.unit_config = config['work_cfg']

        self.state_topic = 'state/{}/{}'.format(self.place_id, self.type)

        self.period = self.unit_config.get('period', 3)
        self.last_send_time = time.time()

        self.sample_data = {
            'temp': 25,
            'humid': 40,
            'light': 90
        }
        # self.device = Pin(2, Pin.OUT)

    def subscribe(self, mqttc):
        pass

    def callback(self, topic, msg):
        print('Callback data: {} / {}'.format(topic, msg))

    def step(self, send):
        ts = time.time()
        if (ts - self.last_send_time) > self.period:
            self.last_send_time = ts

            msg = {
                'device_id': self.device_id,
                'state': {
                    'temperature': self.sample_data['temp'] + m.sin(ts/20),
                    'humidity': self.sample_data['humid'],
                    'lightness': self.sample_data['light']
                }
            }
            send(self.state_topic, msg)

        return True
