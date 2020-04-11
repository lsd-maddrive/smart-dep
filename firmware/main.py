from umqtt.simple import MQTTClient
import ubinascii
import network
import ujson
import time
import dht
from machine import Pin

import env

# Definitions

def get_mac():
    return ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(env.WiFi_SSID, env.WiFi_PASS)
        while not wlan.isconnected():
            pass
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

connect_wifi()

global_config = {
    'mqtt': {
        'server': '192.168.31.90',
        'port': 1883,
        'user': 'rabbitmq',
        'pass': 'rabbitmq'
    },
    'place_id': '8203',
}

mqtt_config = global_config['mqtt']
unique_id = get_mac()
client = MQTTClient(client_id=unique_id,
                    server=mqtt_config['server'],
                    port=mqtt_config['port'],
                    user=mqtt_config['user'],
                    password=mqtt_config['pass'])

def callback(topic, msg):
    for device in devices:
        device._callback(topic, msg)

client.set_callback(callback)
client.connect()

devices = [
    LightControlDevice(global_config, client),
    EnvironmentDevice(global_config, client)
]

while True:
    try:
        for device in devices:
            device.step(client)
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            break
        print(e)
        # break

    time.sleep(1)
