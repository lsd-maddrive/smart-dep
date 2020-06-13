import time
import ujson as json
import machine
import ubinascii

import _utils as ut

from umqtt.simple import MQTTClient

import urequests as requests


def register_device(host, data):
    try:
        url = '{}/api/v1/register'.format(host)
        headers = {
            'Content-Type': 'application/json'
        }
        result = requests.post(url, json=data, headers=headers)
        if result.status_code >= 400:
            return None

        return result.json()
    except Exception as e:
        print('Failed to get registration data: {}'.format(e))

    return None

def enabled_device(host, data):
    try:
        url = '{}/api/v1/enabled'.format(host)
        headers = {
            'Content-Type': 'application/json'
        }
        result = requests.post(url, json=data, headers=headers)
        if result.status_code >= 400:
            return None

        return result.json()
    except Exception as e:
        print('Failed to get registration data: {}'.format(e))

    return None


def main(config):
    CLIENT_ID = ubinascii.hexlify(machine.unique_id())
    device_id = config.get('device_id')

    if device_id is None:
        reg_data = register_device(config['micro_server'], {
            'unique_id': CLIENT_ID
        })

        if reg_data is None:
            print('Failed to register device')
            return -1

        device_id = reg_data['device_id']

        local_config = {'device_id': device_id}
        ut.set_config(local_config)
        print('Device received device_id ({}) - restart'.format(device_id))
        return 1
    else:
        # Register enable of device
        ifconfig = ut.connect_wifi(config)
        ip_addr = ifconfig[0]
        data = {
            'unique_id': CLIENT_ID,
            'device_id': device_id,
            'ip_addr': ip_addr,
        }
        print('Send enabled state: {}'.format(data))
        reg_data = enabled_device(config['micro_server'], data)

    # After DeviceID is in system - we can start processing
    mqtt_config = config['mqtt']
    print('MQTT client id: {}'.format(CLIENT_ID))
    mqttc = MQTTClient(client_id=CLIENT_ID,
                       server=mqtt_config['server'],
                       port=mqtt_config['port'],
                       user=mqtt_config['user'],
                       password=mqtt_config['pass'])

    local_ctx = {
        'reload_required': False
    }

    led = machine.Pin(2, machine.Pin.OUT)

    def mqtt_callback(topic, msg):
        msg = json.loads(msg)
        print('Received message: {} on {}'.format(msg, topic))
        if topic == b'cfg/ping':
            led.value(not led.value())


    mqttc.set_callback(mqtt_callback)
    mqttc.connect()

    mqttc.subscribe('cfg/update')
    mqttc.subscribe('cfg/ping')

    while True:
        mqttc.check_msg()
        time.sleep(1)
