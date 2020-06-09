#!/bin/bash
docker-compose -p local up --build --abort-on-container-exit timescaledb pgadmin apiserver #emulator state_tracker