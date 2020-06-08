import time
import json
import sys
import paho.mqtt.client as mqtt
import yaml
import os

from fluent import handler
import logging

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

fluent_h = handler.FluentHandler('emulator', host='fluentd', port=24224)
formatter = handler.FluentRecordFormatter(custom_format)
fluent_h.setFormatter(formatter)

# Set to all modules (set to root logger)
logging.basicConfig(level=logging.DEBUG,
                    handlers=[std_h, fluent_h])

logger = logging.getLogger('emulator')


# Definitions


class ControlDevice(object):
    def __init__(self, config, type_):
        self.config = config
        self.device_id = config['id']
        self.place_id = config['place_id']
        self.type = type_

        self.cmd_topic = 'cmd/{}/{}'.format(self.place_id, self.type)
        self.cfg_topic = 'cfg/{}/{}'.format(self.place_id, self.type)
        self.state_topic = 'state/{}/{}'.format(self.place_id, self.type)

    def _send_state(self, state, client):
        msg = {
            'type': self.type,
            'device_id': self.device_id,
            'place_id': self.place_id,
            'state': state,
        }
        logger.debug(f'Send state: {msg}')
        client.publish(self.state_topic, json.dumps(msg))

    def _callback(self, topic, data):
        if 'device_id' not in data:
            logger.warning(f'Message has no \'device_id\' field')
            return

        if data['device_id'] != self.device_id:
            return

        if topic == self.cmd_topic:
            logger.debug(f'Command received: {topic} / {data}')
            if 'cmd' not in data:
                logger.warning(f'Message has no \'cmd\' field')
                return

            self._apply_command(data['cmd'])

        elif topic == self.cfg_topic:
            logger.debug(f'Configuration received: {topic} / {data}')
            if 'cfg' not in data:
                logger.warning(f'Message has no \'cfg\' field')
                return

            self._update_config(data['cfg'])

    def _apply_command(self, cmd):
        logger.warning(f'No command handler for {cmd}')

    def _update_config(self, cfg):
        logger.warning(f'No configuration handler for {cfg}')


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

    def _update_config(self, cfg):
        if 'period' not in cfg:
            logger.warning(f'Config has no \'period\' field')
            return

        self.work_config.update(cfg)
        logger.debug(f'Device {self.device_id} applied configuration {cfg}')

    def _apply_command(self, cmd):
        if 'enable' not in cmd:
            logger.warning(f'Command has no \'enable\' field')
            return

        self.is_enabled = cmd['enable']
        logger.debug(f'Device {self.device_id} applied command {cmd}')

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

    def _update_config(self, cfg):
        if 'period' not in cfg:
            logger.warning(f'Config has no \'period\' field')
            return

        self.work_config.update(cfg)
        logger.debug(f'Device {self.device_id} applied configuration {cfg}')

    def _apply_command(self, cmd):
        if 'enable' not in cmd:
            logger.warning(f'Command has no \'enable\' field')
            return

        self.is_enabled = cmd['enable']
        logger.debug(f'Device {self.device_id} applied command {cmd}')

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

    def _update_config(self, cfg):
        if 'period' not in cfg:
            logger.warning(f'Config has no \'period\' field')
            return

        self.work_config.update(cfg)
        logger.debug(f'Device {self.device_id} applied configuration {cfg}')

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
                'lightness': data['light']
            }, client)

        return True

# Utilization

import importlib

class ReloadWrapper():
    def __init__(self):
        self.updateRequired = False
        self.unit = None

    def reload(self):
        self.updateRequired = self.unit is not None

    def _reload(self):
        import intcode
        importlib.reload(intcode)
        self.unit = intcode.Code()
        self.updateRequired = False

    def _load(self):
        try:
            import intcode
            self.unit = intcode.Code()
            return True
        except Exception as e:
            logger.error(f'Error loading: {e}')

        return False

    def get_unit(self):
        if self.unit is None:
            result = self._load()
            if not result:
                return None

        if self.updateRequired:
            self._reload()

        return self.unit

    def get_test_msg(self):
        if self.unit is None:
            result = self._load()
            if not result:
                return None

        if self.updateRequired:
            self._reload()

        return self.unit.test_msg()

def main():
    device_id = os.getenv('DEVICE_ID')
    if device_id is None:
        logger.critical(f'DEVICE_ID not set - exit')
        exit(1)

    reloader = ReloadWrapper()

    with open("config.yml") as f:
        try:
            g_config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            logger.debug(exc)

    app_config = g_config['app']
    mqtt_config = app_config['mqtt']

    def on_message(client, userd, msg):
        try:
            data = json.loads(msg.payload)
            logger.debug(f'Received data: {data}')

            code_str = data['code']
            with open('intcode.py', 'w') as f:
                f.write(code_str)

            logger.debug('Code writed!')
            reloader.reload()
        except Exception as e:
            logger.error(f'Error in callback: {e}')

    def on_connect(client, userd, flags, rc):
        logger.debug(f"Connected with result code {rc} / {userdata}")
        client.subscribe('cfg/updates')

    is_connected = False

    g_client = mqtt.Client(device_id)
    g_client.on_message = on_message
    g_client.on_connect = on_connect
    g_client.username_pw_set(
        username=mqtt_config['username'], password=mqtt_config['password'])

    # Five times reconnection tries
    for i in range(5):
        try:
            g_client.connect(mqtt_config['host'], mqtt_config['port'], 60)
            is_connected = True
            break
        except:
            logger.warning(
                f'Failed to connect to MQTT broker, retry after 10 seconds')
            time.sleep(10)

    if not is_connected:
        logger.error(f'Failed to connect to: {mqtt_config}')
        exit(1)

    logger.debug('Connected to MQTT')
    g_client.subscribe('cfg/updates')
    g_client.loop_start()

    while True:
        try:
            unit = reloader.get_unit()
            if unit is None:
                time.sleep(1)
            else:
                unit.step(g_client)
        except Exception as e:
            logger.error(f'Error in steps: {e}')
            if type(e) == KeyboardInterrupt:
                break

        time.sleep(1)


if __name__ == '__main__':
    main()
