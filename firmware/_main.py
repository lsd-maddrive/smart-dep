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
        'ssid': 'smartdepwifi',
        'pass': '1234_smartdepwifi_pass'
    },
    'mqtt': {
        'server': '192.168.31.175',
        'port': 1883,
        'user': 'rabbitmq',
        'pass': 'rabbitmq'
    },
    'micro_server': 'http://192.168.31.175:5001'
}


file_config = ut.get_config()
if file_config is not None:
    g_config.update(file_config)

ifconfig = ut.connect_wifi(g_config)


def import_app():
    from last.app import main
    return main


def perform_update(config, check_versions=True):
    update_version = None

    if check_versions:
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

# TODO - for debug we always perform update to last version after reset
if perform_update(g_config, check_versions=False):
    print('Module updated')
else:
    print('Update failed - reset')
    time.sleep(10)
    machine.reset()

while True:
    try:
        main = import_app()
    except Exception as e:
        print('Failed to import main() - WTF?')
        break

    try:
        ret = main(g_config)
        if ret != 0:
            machine.reset()
    except Exception as e:
        print('main() execution failed: {}'.format(e))
        machine.reset()

    time.sleep(10)
