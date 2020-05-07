#!/bin/bash
python3 migration_manager.py db migrate
python3 migration_manager.py db upgrade
 