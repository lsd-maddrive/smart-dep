#!/usr/bin/env bash

ampy --port /dev/ttyUSB0 put env.json
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 ls

# rshell -p /dev/ttyUSB0 cp main.py /main.py
# rshell -p /dev/ttyUSB0 cp env.json /env.json
# rshell -p /dev/ttyUSB0 ls /
