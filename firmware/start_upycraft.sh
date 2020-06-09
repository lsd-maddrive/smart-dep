#!/bin/bash

# XAUTH=/tmp/.docker.xauth
# XSOCK=/tmp/.X11-unix

xhost +local:root

docker build -t upycraft:latest -f Dockerfile.upycraft . && \
docker run --rm -ti \
        -e QT_X11_NO_MITSHM=1 \
        -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
        --device=/dev/ttyUSB0 \
        upycraft:latest

# docker run --rm -it \
        # -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH \
        # upycraft:latest

xhost -local:root
