#!/bin/bash
docker-compose -p local up --build --abort-on-container-exit timescaledb apiserver

# emulator state_tracker pgadmin