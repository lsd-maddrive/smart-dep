#!/bin/bash

# to fix RuntimeError: command not found: initdb 
# instal postgresql 
# sudo apt-get install postgresql  

cd tests 
pip3 install -r requirements.txt 
pytest