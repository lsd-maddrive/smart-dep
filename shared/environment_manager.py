import os
import sys 

from dotenv import load_dotenv
from pathlib import Path

def set_env(argv):
    if argv == 'test':
        env_path = Path('./testing') /'.env.test'
    elif argv == 'dep':
        # TO DO: path to .env.dep
        env_path = ''
        pass
    else:
        # TO DO: set default settings in the future 
        env_path = Path('./testing') /'.env.test'
    
    return env_path

try:
    load_dotenv(dotenv_path=set_env(sys.argv[1]))
except IndexError as err:
    # TO DO: set default settings in the future 
    load_dotenv(dotenv_path=set_env('test'))
