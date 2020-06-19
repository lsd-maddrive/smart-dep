#!/bin/bash
docker-compose -p local up --build --abort-on-container-exit timescaledb pgadmin apiserver web # emulator state_tracker