import time


class Code():
    def __init__(self, config):
        self.config = config
        self.device_id = config['device_id']
        self.place_id = config['place_id']
        self.type = config['type']
        self.unit_config = config['work_cfg']

        self.cmd_topic = 'cmd/{}/{}'.format(self.place_id, self.type)
        self.state_topic = 'state/{}/{}'.format(self.place_id, self.type)

        self.period = self.unit_config.get('period', 3)
        self.last_send_time = time.time()

        self.is_enabled = False
        # self.device = Pin(2, Pin.OUT)

    def subscribe(self, mqttc):
        print('Subscribe to {}'.format(self.cmd_topic))
        mqttc.subscribe(self.cmd_topic)

    def callback(self, topic, msg):
        print('Callback data: {} / {}'.format(topic, msg))
        device_id = msg.get('device_id')

        if topic == self.cmd_topic:
            if device_id != self.device_id:
                return

            cmd = msg.get('data')
            if cmd is None:
                return

            enable = cmd.get('enable')
            if enable is None:
                return

            self.is_enabled = enable
            # To send permanently
            self.last_send_time = -1
            print('Device ({}) switched to {}'.format(
                self.device_id, self.is_enabled))

    def step(self, send):
        # if not self.is_enabled:
        #     self.device.on()
        # else:
        #     self.device.off()

        ts = time.time()
        if (ts - self.last_send_time) > self.period or \
                self.last_send_time < 0:

            self.last_send_time = ts

            msg = {
                'device_id': self.device_id,
                'state': {
                    'enabled': self.is_enabled
                }
            }
            send(self.state_topic, msg)

        return True
