#!/bin/bash

export PYTHONPATH=$PYTHONPATH:..
export $(cat ../config/.env.dev | xargs)
export RABBITMQ_URI="amqp://rabbitmq:rabbitmq@localhost:5672/%2F"
export DB_URI="postgresql+psycopg2://admin:admin@localhost:5432/smart_dep"
python app.py
