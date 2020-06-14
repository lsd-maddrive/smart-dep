import importlib
import time
import json
import sys
import paho.mqtt.client as mqtt
import yaml
import os
import socket
import requests

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

# Try to make same code as from units/app_code.py


def register_device(host, data):
    try:
        url = '{}/api/v1/app/register'.format(host)
        headers = {
            'Content-Type': 'application/json'
        }
        result = requests.post(url, json=data, headers=headers)
        if result.status_code >= 400:
            logger.debug('Received status code: {}'.format(result.status_code))
            return None

        return result.json()
    except Exception as e:
        logger.debug('Failed to get registration data: {}'.format(e))

    return None


def enable_device(host, data):
    try:
        url = '{}/api/v1/app/enabled'.format(host)
        headers = {
            'Content-Type': 'application/json'
        }
        result = requests.post(url, json=data, headers=headers)
        if result.status_code >= 400:
            logger.debug('Received status code: {}'.format(result.status_code))
            if result.status_code == 403:
                return None, True

        return result.json(), False
    except Exception as e:
        logger.debug('Failed to get enable data: {}'.format(e))

    return None, False


def receive_subapp_code(host, device_type):
    try:
        url = '{}/api/v1/app/unit_code?devtype={}'.format(host, device_type)
        result = requests.get(url)
        if result.status_code >= 400:
            logger.debug('Received status code: {}'.format(result.status_code))
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
        logger.debug('Failed to get unit code: {}'.format(e))

    return None

# Utilization


g_config = {
    'mqtt': {
        'server': 'rabbitmq',
        'port': 1883,
        'user': 'rabbitmq',
        'pass': 'rabbitmq'
    },
    'micro_server': 'http://microserver:8080'
}


def main():
    hostname = socket.gethostname()
    logger.debug(f'Hostname: {hostname}')

    unique_id = f'emulator-device-{hostname}'
    # unique_id = os.getenv('UNIQUE_ID')
    # if unique_id is None:
    #     logger.critical(f'UNIQUE_ID not set - exit')
    #     return 1

    reg_data = register_device(g_config['micro_server'], {
        'unique_id': unique_id
    })
    logger.debug(f'Received register data: {reg_data}')

    if reg_data is None:
        logger.error(f'Failed to register device with {unique_id}, reset')
        return 1

    device_id = reg_data['device_id']
    ip_addr = socket.gethostbyname(hostname)

    en_data, reg_required = enable_device(g_config['micro_server'], {
        'unique_id': unique_id,
        'device_id': device_id,
        'ip_addr': ip_addr,
    })
    logger.debug(f'Received enable data: {en_data}')

    if reg_required:
        logger.error(f'Server requested to update registration, reset')
        return 1

    if en_data is None:
        logger.error(
            f'Failed to enable device with {unique_id}/{device_id}, reset')
        return 1

    unit_code = None

    device_type = en_data.get('type')
    if device_type is not None:
        constr = receive_subapp_code(g_config['micro_server'], device_type)
        if constr is not None:
            unit_config = {
                'device_id': device_id,
                'place_id': en_data.get('place_id'),
                'work_cfg': en_data.get('config'),
                'type': device_type
            }
            unit_code = constr(unit_config)
    else:
        logger.debug('Device type not set - install device first')

    mqtt_config = g_config['mqtt']

    def on_message(mqttc, userd, msg):
        try:
            topic = msg.topic
            data = json.loads(msg.payload)
            logger.debug(
                f'Device {unique_id} received data: {data} via topic: {topic}')

            if topic == 'cfg/ping':
                if data['device_id'] == device_id:
                    logger.debug(f'Device {unique_id} received ping')
                    return
            elif topic == 'cfg/reset':
                if data['device_id'] == device_id:
                    local_ctx['reload_required'] = True
                    return

            if unit_code is not None:
                unit_code.callback(topic, data)

        except Exception as e:
            logger.error(f'Error in callback: {e}')

    def on_connect(mqttc, userd, flags, rc):
        logger.debug(f"Connected with result code {rc} / {userdata}")
        subscribe(mqttc)

    def subscribe(mqttc):
        mqttc.subscribe('cfg/reset')
        mqttc.subscribe('cfg/ping')

    is_connected = False

    mqttc = mqtt.Client(unique_id)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.username_pw_set(
        username=mqtt_config['user'], password=mqtt_config['pass'])

    local_ctx = {
        'reload_required': False
    }

    # Five times reconnection tries
    for i in range(5):
        try:
            mqttc.connect(mqtt_config['server'], mqtt_config['port'], 60)
            is_connected = True
            break
        except Exception as e:
            logger.warning(
                f'Failed to connect to MQTT broker: {e}, retry after 10 seconds')
            time.sleep(10)

    if not is_connected:
        logger.error(f'Failed to connect to: {mqtt_config}')
        return 1

    logger.debug(f'Connected to MQTT')
    subscribe(mqttc)
    mqttc.loop_start()

    def send(topic, data):
        mqttc.publish(topic, json.dumps(data))

    if unit_code is not None:
        res = unit_code.subscribe(mqttc)

    while True:
        if local_ctx['reload_required']:
            return 1

        if unit_code is not None:
            res = unit_code.step(send)

        time.sleep(0.1)


if __name__ == '__main__':
    sys.exit(main())
