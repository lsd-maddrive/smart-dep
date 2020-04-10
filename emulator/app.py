import time
import json
import paho.mqtt.client as mqtt
import yaml

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Definitions


class ControlDevice(object):
    def __init__(self, config, type_):
        self.config = config
        self.unique_id = config['mac']
        self.place_id = config['place_id']

        self.cmd_topic = 'cmd/{}/{}'.format(self.place_id, type_)
        self.cfg_topic = 'cfg/{}/{}'.format(self.place_id, type_)
        self.state_topic = 'state/{}/{}'.format(self.place_id, type_)

    def _send_state(self, state, client):
        msg = {
            'type': 'env',
            'device_id': self.unique_id,
            'place_id': self.place_id,
            'state': state,
        }
        logger.debug(f'Send state: {msg}')
        client.publish(self.state_topic, json.dumps(msg))


class LightControlDevice(ControlDevice):
    def __init__(self, config, client):
        super().__init__(config, 'light')
        self.config = config

        client.subscribe(self.cmd_topic)
        client.subscribe(self.cfg_topic)

        self.work_config = {
            'period': 5    # [s]
        }

        self.last_send_time = time.time()
        self.is_enabled = False

    def _update_config(self, config):
        if 'period' not in config:
            logger.warning(f'Config has no \'period\' field')
            return

        self.work_config = config
        logger.debug(f'Configuration applied: {config}')

    def _callback(self, topic, msg):
        if topic == self.cmd_topic:
            data = json.loads(msg)
            logger.debug(f'Command received: {topic} / {data}')
            if 'cmd' not in data:
                logger.warning(f'Message has no \'cmd\' field')
                return

            cmd = data['cmd']
            if 'enable' not in cmd:
                logger.warning(f'Command has no \'enable\' field')
                return

            self.is_enabled = cmd['enable']
        elif topic == self.cfg_topic:
            data = json.loads(msg)
            logger.warning(f'Configuration received: {topic} / {data}')
            if 'cfg' not in data:
                logger.warning(f'Message has no \'cfg\' field')
                return

            self._update_config(data['cfg'])

    def step(self, client):
        ts = time.time()
        if ts - self.last_send_time > self.work_config['period']:
            self.last_send_time = ts
            self._send_state({
                'enabled': self.is_enabled
            }, client)

        return True


class PowerControlDevice(ControlDevice):
    def __init__(self, config, client):
        super().__init__(config, 'power')
        self.config = config

        client.subscribe(self.cmd_topic)
        client.subscribe(self.cfg_topic)

        self.work_config = {
            'period': 5    # [s]
        }

        self.last_send_time = time.time()
        self.is_enabled = False

    def _update_config(self, config):
        if 'period' not in config:
            logger.warning(f'Config has no \'period\' field')
            return

        self.work_config = config
        logger.debug(f'Configuration applied: {config}')

    def _callback(self, topic, msg):
        if topic == self.cmd_topic:
            data = json.loads(msg)
            logger.debug(f'Command received: {topic} / {data}')
            if 'cmd' not in data:
                logger.warning(f'Message has no \'cmd\' field')
                return

            cmd = data['cmd']
            if 'enable' not in cmd:
                logger.warning(f'Command has no \'enable\' field')
                return

            self.is_enabled = cmd['enable']
        elif topic == self.cfg_topic:
            data = json.loads(msg)
            logger.warning(f'Configuration received: {topic} / {data}')
            if 'cfg' not in data:
                logger.warning(f'Message has no \'cfg\' field')
                return

            self._update_config(data['cfg'])

    def step(self, client):
        ts = time.time()
        if ts - self.last_send_time > self.work_config['period']:
            self.last_send_time = ts
            self._send_state({
                'enabled': self.is_enabled
            }, client)

        return True


class EnvironmentDevice(ControlDevice):
    def __init__(self, config, client):
        super().__init__(config, 'env')
        self.config = config

        client.subscribe(self.cfg_topic)

        self.work_config = {
            'period': 5    # [s]
        }

        self.last_send_time = time.time()
        self.is_enabled = False

    def _update_config(self, config):
        if 'period' not in config:
            logger.warning(f'Config has no \'period\' field')
            return

        self.work_config = config
        logger.debug(f'Configuration applied: {config}')

    def _callback(self, topic, msg):
        if topic == self.cfg_topic:
            data = json.loads(msg)
            logger.warning(f'Configuration received: {topic} / {data}')
            if 'cfg' not in data:
                logger.warning(f'Message has no \'cfg\' field')
                return

            self._update_config(data['cfg'])

    def _device_get_data(self):
        return {
            'temp': 25,
            'humid': 40,
            'light': 35
        }

    def step(self, client):
        ts = time.time()
        if ts - self.last_send_time > self.work_config['period']:
            self.last_send_time = ts

            data = self._device_get_data()
            self._send_state({
                'temperature': data['temp'],
                'humidity': data['humid'],
                'lighntess': data['light']
            }, client)

        return True

# Utilization


with open("config.yml") as f:
    try:
        g_config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        logger.debug(exc)

app_config = g_config['app']
mqtt_config = app_config['mqtt']


def callback(mqttc, obj, msg):
    for device in devices:
        device._callback(msg.topic, msg.payload)


g_client = mqtt.Client()
g_client.on_message = callback
g_client.username_pw_set(username=mqtt_config['username'], password=mqtt_config['password'])
g_client.connect(mqtt_config['host'], mqtt_config['port'], 60)

logger.debug('Connected to MQTT')


def get_device(device_name, config, client):
    type_ = config['type']

    types = {
        'light': LightControlDevice,
        'power': PowerControlDevice,
        'env': EnvironmentDevice
    }

    if type_ not in types:
        return None

    return types[type_](config, client)


devices = []
for device_name, device_config in app_config['devices'].items():
    device = get_device(device_name, device_config, g_client)
    if device:
        logger.debug(f'Created device: {device}')
        devices.append(device)

g_client.loop_start()

while True:
    try:
        for device in devices:
            device.step(g_client)
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            break
        logger.error(e)

    time.sleep(1)