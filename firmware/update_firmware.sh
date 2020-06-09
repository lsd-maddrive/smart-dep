#!/bin/bash

DEVICE=/dev/ttyUSB0
docker build -t firmware_upy:latest . && \
docker run --rm -ti --device $DEVICE -e DEVICE=$DEVICE firmware_upy:latest
