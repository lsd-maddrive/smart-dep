from datetime import datetime  
import os
import sys 
sys.path.append("..")

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from shared.models.table_models import db, Commands, Params, States 

load_dotenv()

def create_app():
    app = Flask(__name__)
    env_mode = os.getenv('SMART_ENV', 'dev')
    config_path = f'../shared/config/{env_mode}/config.py'
    
    app.config.from_pyfile(config_path)
    db.init_app(app)
    return app

'''
    @brief:     Add new row in specified table
    @args:      Obj     - name of table (class)
                item    - Class object with parameters
                info    = True print information about 
                        new row 
                        = False no printed information 
'''
def add_new_row(Obj, item, info=False):
    with app.app_context():
        check_item = Obj.query.filter_by(id=item.id).first()
        # if row doesnt's exist 
        if check_item == None:
            db.session.add(item)
            db.session.commit() 
            if info:
                print(f"New row was added in table {Obj.__name__}")
        else:
            print(f"Item with ID: {item.id} already exists in the table {Obj.__name__}.")

'''
    @brief:     Update value of the specified field in the specified table
    @args:      Obj     - name of table (Class)
                id      - id number of row 
                field   - name of field to be updated
                val     - new value of field  
'''
def update_item(Obj, id, field, val):
    with app.app_context():
        com = Obj.query.filter_by(id=id).first()
        if com != None:
            if field == 'timestamp':
                if com.timestamp != val:
                    com.timestamp = val
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
            elif field == 'command':
                if com.command != val:
                    com.command = val 
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
            elif field == 'params':
                if com.params != val:
                    com.params = val 
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
            elif field == 'state':
                if com.state != val:
                    com.state = val
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
            elif field == 'device_id':
                if com.device_id != val:
                    com.device_id = val 
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
            elif field == 'place_id':
                if com.place_id != val:
                    com.place_id = val 
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
            elif field == 'type':
                if com.type != val:
                    com.type = val 
                    db.session.commit()
                else:
                    print(f"The value of the {field} isn't changed")
        else:
            print(f"Item {id} doesn't exist in the table {Obj.__name__}")

'''
    @brief:     Delete specified row in table 
    @args:      Obj - name of table (Class)
                id  - id number of the row 
                info    = True print information about 
                        removed row in the table 
                        = False no printed information 
'''       
def delete_item(Obj, id, info=False):
    with app.app_context():
        com = Obj.query.filter_by(id=id).first()
        if com != None:
            db.session.delete(com)
            db.session.commit()
            if info:
                print(f"Row ID: {id} was removed from table {Obj.__name__}")
        else:
            print(f"Item ID: {id} doesn't exist in the table {Obj.__name__} ")

'''
    @brief:     Delete all rows in specified table
    @args:      Obj     - name of table (Class)      
                info    = True print information about 
                        number of deleted rows in the table 
                        = False no printed information 
'''
def delete_all_items(Obj, info=False):
    with app.app_context():
        del_num = Obj.query.delete()
        if info:
            print(f"{del_num} items was removed from table {Obj.__name__}")
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        
    new_command = Commands(id=1, timestamp=datetime.now(), 
                           command={}, device_id="test1", 
                           place_id="8206", type="Power")
    new_param = Params(id=1, timestamp=datetime.now(),
                       params={}, device_id="test2",
                       place_id="8201", type="Env")
    new_state = States(id=1, timestamp=datetime.now(),
                       state={}, device_id="test3", 
                       place_id="8101", type="Light")

    add_new_row(Commands, new_command)
    add_new_row(Params, new_param)
    add_new_row(States, new_state)

    update_item(Commands, 1, 'place_id', "8203-1")
    update_item(Params, 1, 'type', 'Power')
    update_item(States, 1, 'device_id', "test4")

    delete_all_items(Commands, info=True)
    delete_item(Params, 1)
    delete_all_items(States, info=True)
    delete_all_items(Params, info=True)

  