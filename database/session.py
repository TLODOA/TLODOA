from sqlalchemy import MetaData, text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

##
def database_create(engine:object)->object:
    with open('./database/casts/schema.sql', 'r') as file:
        sql = file.read()

    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base(metadata=metadata)
    return Base

def database_drop_tables(engine:object)->None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(engine)


"""
def reset_database(Base:object, engine:object):
    Base.metadata.drop_all(engine)
    
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # Base.metadata.create_all(engine)
"""

engine = create_engine("postgresql://lorax:@localhost/tlodoadb", echo=True)

database_drop_tables(engine)
Base = database_create(engine)

Session = sessionmaker(bind=engine)
session = Session()
