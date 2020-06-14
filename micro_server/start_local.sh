#!/bin/bash

export PYTHONPATH=$PYTHONPATH:../db
export $(cat ../config/.env.dev | xargs)
export DB_URI=postgresql+psycopg2://admin:admin@localhost:5432/smart_dep
python app.py
