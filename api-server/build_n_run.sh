#!/usr/bin/env bash

NAME=backend
TAG=local_test
IMAGE=$NAME:$TAG

docker build -t $IMAGE . && \
docker run --rm -it -p 8080:8080 --name=$NAME $IMAGE
