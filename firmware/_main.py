import network
import ujson
import time
import dht
from machine import Pin
from machine import reset
import sys
import os

import _utils as ut

g_config = {
    'wifi': {
        'ssid': '',
        'pass': ''
    },
    'mqtt': {
        'server': 'tigra-acs.duckdns.org',
        'port': 1883,
        'user': 'rabbitmq',
        'pass': 'rabbitmq'
    },
    'micro_server': 'http://192.168.31.175:5001'
}

# Definitions


def connect_wifi(config):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config['wifi']['ssid'], config['wifi']['pass'])
        while not wlan.isconnected():
            time.sleep(1)
    print('network config:', wlan.ifconfig())


class ControlDevice(object):
    def __init__(self, config, type_):
        self.config = config

        self.cmd_topic = 'cmd/{}/{}'.format(config['place_id'], type_)
        self.cfg_topic = 'cfg/{}/{}'.format(config['place_id'], type_)
        self.state_topic = 'state/{}/{}'.format(config['place_id'], type_)


class LightControlDevice(ControlDevice):
    def __init__(self, config, client):
        super().__init__(config, 'light')
        self.config = config

        self.unique_id = get_mac()
        client.subscribe(self.cmd_topic)
        client.subscribe(self.cfg_topic)

        self.work_config = {
            'period': 5    # [s]
        }

        self.last_send_time = time.time()
        self.is_enabled = False

        self.device = Pin(2, Pin.OUT)

    def _callback(self, topic, msg):
        data = ujson.loads(msg)
        print('Data: {} / {} / {}'.format(topic, msg, data))

    def _send_state(self, state, client):
        msg = {
            'type': 'light',
            'device_id': self.unique_id,
            'state': state
        }
        client.publish(self.state_topic, ujson.dumps(msg))

    def step(self, client):
        if not self.is_enabled:
            self.device.on()
        else:
            self.device.off()

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

        self.unique_id = get_mac()
        client.subscribe(self.cfg_topic)

        self.dev = dht.DHT11(Pin(15))

        self.work_config = {
            'period': 5    # [s]
        }

        self.last_send_time = time.time()
        self.is_enabled = False

    def _callback(self, topic, msg):
        data = ujson.loads(msg)
        print('Data: {} / {} / {}'.format(topic, msg, data))

    def _send_state(self, state, client):
        msg = {
            'type': 'env',
            'device_id': self.unique_id,
            'state': state,
        }
        client.publish(self.state_topic, ujson.dumps(msg))

    def step(self, client):
        ts = time.time()
        if ts - self.last_send_time > self.work_config['period']:
            self.last_send_time = ts
            self.dev.measure()
            temp = self.dev.temperature()
            humid = self.dev.humidity()
            self._send_state({
                'temperature': temp,
                'humidity': humid,
                'lighntess': 0
            }, client)

        return True

# Utilization

file_config = ut.get_config()
if file_config is not None:
    g_config.update(file_config)

connect_wifi(g_config)

# device = Pin(2, Pin.OUT)
# device.on()


def import_app():
    from last.app import main
    return main


def perform_update(config):
    update_version = None
    c_ver = ut.get_current_version()
    # If current version not exists - update to last one
    if c_ver is not None:
        print('Current version: {}'.format(c_ver))
        # There is current version - compare with planned version
        n_ver = ut.get_next_version()
        print('Next version: {}'.format(n_ver))
        if n_ver is None:
            print('No next version')
            # No next version - no need to update
            return True

        if c_ver == n_ver:
            print('Versions are equal')
            # Versions are equal - ok
            return True
        else:
            update_version = n_ver

    print('Start downloading update')
    result = ut.get_app(config['micro_server'], update_version)
    if not result:
        # Failed to receive code or validation failed
        return False

    ut.rename_dir('next', 'last')
    print('Full update completed')
    return True


main = None

while True:
    if perform_update(g_config):
        print('Module updated')
    else:
        print('Update failed - soft reset')
        time.sleep(10)
        break

    try:
        main = import_app()
    except Exception as e:
        print('Failed to import main() - WTF?')
        break

    try:
        ret = main(g_config)
        # Success return - soft reset
        if ret == 0:
            break
    except Exception as e:
        print('main() execution failed: {}'.format(e))

    time.sleep(1)
