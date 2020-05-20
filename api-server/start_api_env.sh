#!/bin/bash
docker-compose -p local up --build --abort-on-container-exit timescaledb pgadmin emulator state_tracker apiserver

# emulator state_tracker pgadmin