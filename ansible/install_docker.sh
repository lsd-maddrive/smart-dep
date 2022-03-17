#!/bin/bash

ansible-playbook playbooks/install-docker-playbook.yml -c local --ask-become-pass -e ansible_python_interpreter=/usr/bin/python3
