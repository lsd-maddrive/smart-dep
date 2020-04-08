#!/usr/bin/env bash

NAME=ui
TAG=local_test
IMAGE=$NAME:$TAG

rm -rf app/node_modules
docker build -t $IMAGE .

docker run --rm -it -p 8080:80 --name=$NAME $IMAGE
