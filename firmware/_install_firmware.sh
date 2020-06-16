#!/bin/bash

esptool.py --port=$DEVICE erase_flash && \
esptool.py --port=$DEVICE --baud 460800 write_flash --flash_size=detect 0 firmware.bin
