from datetime import datetime  
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys 
sys.path.append("..")

from shared.models.table_models import metadata, Commands, Configs, States 

env_mode = os.getenv('SMART_ENV', 'dev')
config_path = f'shared.config.{env_mode}.config'

with open(f'../shared/config/{env_mode}/config.py') as cfg_file:
    db_uri = cfg_file.readline().split("'")[1]

if __name__ == "__main__":
    engine = create_engine(db_uri)
    session = Session(engine)


    new_command = Commands(timestamp=datetime.now(), 
                           command={}, device_id="test1", 
                           place_id="8206", type="Power")
    new_cfg = Configs(timestamp=datetime.now(),
                       config={}, device_id="test2",
                       place_id="8201", type="Env")
    new_state = States(timestamp=datetime.now(),
                       state={}, device_id="test3", 
                       place_id="8101", type="Light")

    session.add(new_command)
    session.add(new_cfg)
    session.add(new_state)

    clear_all = True 
    if clear_all:
        session.query(Commands).delete()
        session.query(Configs).delete()
        session.query(States).delete()

    session.commit() 
    session.close()

  