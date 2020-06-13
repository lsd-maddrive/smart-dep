import time
import ujson as json
import machine
import ubinascii

import _utils as ut

from umqtt.simple import MQTTClient

import urequests as requests


def register_device(host, data):
    try:
        url = '{}/api/v1/app/register'.format(host)
        headers = {
            'Content-Type': 'application/json'
        }
        result = requests.post(url, json=data, headers=headers)
        if result.status_code >= 400:
            print('Received status code: {}'.format(result.status_code))
            return None

        return result.json()
    except Exception as e:
        print('Failed to get registration data: {}'.format(e))

    return None


def enable_device(host, data):
    try:
        url = '{}/api/v1/app/enabled'.format(host)
        headers = {
            'Content-Type': 'application/json'
        }
        result = requests.post(url, json=data, headers=headers)
        if result.status_code >= 400:
            print('Received status code: {}'.format(result.status_code))
            if result.status_code == 403:
                return None, True

        return result.json(), False
    except Exception as e:
        print('Failed to get registration data: {}'.format(e))

    return None, False

def receive_subapp_code(host, device_type):
    try:
        url = '{}/api/v1/app/unit_code?devtype={}'.format(host, device_type)
        result = requests.get(url)
        if result.status_code >= 400:
            print('Received status code: {}'.format(result.status_code))
            return None

        data = result.json()
        code_str = data.get('code')
        if code_str is None:
            return None

        with open('unit.py', 'w') as f:
            f.write(code_str)

        # Sanity check
        from unit import Code
        return Code
    except Exception as e:
        print('Failed to get registration data: {}'.format(e))

    return None

def main(config):
    CLIENT_ID = ubinascii.hexlify(machine.unique_id())
    device_id = config.get('device_id')
    unit_code = None

    if device_id is None:
        reg_data = register_device(config['micro_server'], {
            'unique_id': CLIENT_ID
        })

        if reg_data is None:
            print('Failed to register device')
            return 0

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
        en_data, reg_required = enable_device(config['micro_server'], data)
        if reg_required:
            # Reset config to unregistered
            print('Register required - reset')
            ut.set_config({})
            return 1

        print('Received data after enabled: {}'.format(en_data))
        if en_data is None:
            print('Failed to enable device')
            return 0

        device_type = en_data.get('type')
        if device_type is not None:
            constr = receive_subapp_code(config['micro_server'], device_type)
            if constr is not None:
                unit_config = {
                    'device_id': device_id,
                    'place_id': en_data.get('place_id'),
                    'work_cfg': en_data.get('config'),
                    'type': device_type
                }
                unit_code = constr(unit_config)
        else:
            print('Device type not set - install device first')


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
            return
        elif topic == b'cfg/reset':
            local_ctx['reload_required'] = True
            return

        if unit_code is not None:
            unit_code._callback(topic, msg)

    mqttc.set_callback(mqtt_callback)
    mqttc.connect()

    mqttc.subscribe('cfg/update')
    mqttc.subscribe('cfg/ping')

    while True:
        if local_ctx['reload_required']:
            return 1

        if unit_code is not None:
            res = unit_code.step(mqttc)

        mqttc.check_msg()
        time.sleep(0.1)
