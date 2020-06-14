import time
import ujson as json
from machine import Pin

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
        self.device = Pin(2, Pin.OUT)

    def subscribe(self, mqttc):
        mqttc.subscribe(self.cmd_topic)
        mqttc.subscribe(self.cfg_topic)

    def _callback(self, topic, msg):
        print('Callback data: {} / {}'.format(topic, msg))
        device_id = msg.get('device_id')
        if device_id == self.device_id:
            cmd = msg.get('cmd')
            if cmd is None:
                return

            enable = cmd.get('enable')
            if enable is None:
                return

            self.is_enabled = enable

    def _send_state(self, state, mqttc):
        msg = {
            'device_id': self.device_id,
            'state': state
        }
        mqttc.publish(self.state_topic, json.dumps(msg))

    def step(self, mqttc):
        # if not self.is_enabled:
        #     self.device.on()
        # else:
        #     self.device.off()

        ts = time.time()
        if ts - self.last_send_time > self.period:
            self.last_send_time = ts
            self._send_state({
                'enabled': self.is_enabled
            }, mqttc)

        return True
