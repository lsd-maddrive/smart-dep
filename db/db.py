import os 

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import scoped_session, sessionmaker

from models import metadata, Model 

# db_uri = os.getenv('DB_URI')
# engine = create_engine(db_uri)

# db_session = scoped_session(sessionmaker(
#                             autocommit=False,
#                             autoflush=False,
#                             bind=engine)
# )

# metadata = MetaData() 
# Model = declarative_base(metadata=metadata)
# db = scoped_session(sessionmaker(autocommit=False,
#                                  autoflush=False,
#                                  bind=engine))

db = SQLAlchemy(metadata=metadata)